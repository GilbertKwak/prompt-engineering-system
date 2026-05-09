#!/usr/bin/env python3
"""
pe7_product_mece_loop.py — PE-7 Product Idea → MECE 자동분석 루프
Version : 1.1 | Date: 2026-05-09
Author  : Gilbert

Changelog v1.1:
  - pe3_product_validator.validate() 인라인 통합 (Step 3.5)
  - QC 점수 → Notion PE3 Score 자동 기록 (GPT 자가채점 대체)
  - --dry-run: Notion/OpenAI API 미호출, QC 로직은 실행
  - --qc-only: 로컬 .md 파일 대상 QC 단독 실행 (API 불필요)
  - --qc-strict: 88점 미만 시 Notion 업데이트 중단

Pipeline v1.1:
  Notion DB 폴링
    → '⏳ 대기중' 레코드 감지
    → PE-PROD-ORCH 프롬프트 조합
    → OpenAI API 호출 (gpt-4o)
    → [NEW] PE-3-PROD QC 자동 검증 ← ★
    → 분석 초안 Notion 하위 페이지 생성
    → DB 레코드 업데이트 (PE3 Score 포함)
    → GitHub Issue 등록 (선택)

Usage:
  python pe7_product_mece_loop.py                   # 폴링 1회
  python pe7_product_mece_loop.py --watch            # 60초 간격 반복
  python pe7_product_mece_loop.py --dry-run          # API 미호출, QC만 실행
  python pe7_product_mece_loop.py --qc-only --file <f.md>  # 로컬 파일 QC만
  python pe7_product_mece_loop.py --qc-strict        # 88점 미만 중단
  python pe7_product_mece_loop.py --record-id <id>   # 특정 레코드만 처리

Env vars required:
  NOTION_TOKEN      — Notion Integration Token
  OPENAI_API_KEY    — OpenAI API Key
  GITHUB_TOKEN      — (선택) GitHub Issue 등록용
  NOTION_DB_ID      — Product Ideas DB ID
                      (기본: e34f78c6-d1df-4575-8a2f-a45d716c593e)
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

# ── PE-3-PROD QC 모듈 동적 임포트 ───────────────────────────────────────────
_QC_AVAILABLE = False
try:
    # 실행 위치가 repo root일 때 (GitHub Actions / 로컬 모두 대응)
    _this_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(_this_dir))
    from pe3_product_validator import validate as _qc_validate, BUILTIN_CHECKS, load_checks
    _QC_AVAILABLE = True
except ImportError:
    pass  # QC 모듈 없으면 경고만 출력, 파이프라인은 계속 실행


# ── 환경변수 ─────────────────────────────────────────────────────────────────
NOTION_TOKEN  = os.environ.get("NOTION_TOKEN", "")
OPENAI_KEY    = os.environ.get("OPENAI_API_KEY", "")
GITHUB_TOKEN  = os.environ.get("GITHUB_TOKEN", "")
DB_ID         = os.environ.get("NOTION_DB_ID",
                               "e34f78c6-d1df-4575-8a2f-a45d716c593e")
GH_REPO       = os.environ.get("GITHUB_REPO",
                               "GilbertKwak/prompt-engineering-system")
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL_SEC", "60"))

NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

# QC 체크리스트 경로 (repo root 기준)
_CHECKLIST_YAML = Path(__file__).resolve().parent.parent / "config" / "pe3_product_checklist.yaml"


# ── MECE 분석 프롬프트 템플릿 (PE-PROD-ORCH v1.0) ────────────────────────────
SYSTEM_PROMPT = """당신은 McKinsey/BCG급 신사업 기획 전문가이자 MECE 분석 AI입니다.
PE-PROD-ORCH v1.0 파이프라인을 실행합니다.
Temperature: 0.1 (구조 설계) / 출력 포맷은 반드시 아래 표준 템플릿을 따릅니다."""

USER_PROMPT_TEMPLATE = """PE-PROD-ORCH v1.0 전체 파이프라인을 실행해줘.

분석 대상  : {idea_name}
주체 유형  : {actor_type}
도메인     : {domain}
분석 깊이  : {depth}
목표 IRR   : {target_irr}
PE-FIN 연동: Yes

---

## 출력 표준 포맷 (반드시 준수)

===========================================
📦 {idea_name} — PE-PROD 표준 분석 보고서
분석일: {today} | 버전: v1.0
PE-PROD-ORCH | 분석 모드: {depth}
===========================================

[1/5] MECE 기회 공간 맵 (Layer A~E)
- Layer A (고객): ...
- Layer B (문제): ...
- Layer C (솔루션): ...
- Layer D (수익): ...
- Layer E (경쟁): ...

[2/5] 시장 규모 (TAM/SAM/SOM)
- TAM: $___B (출처: ___)
- SAM: $___B
- SOM (3년): $___M

[3/5] 기술 실현가능성 (TRL ___/9)
- 핵심 기술 리스크 Top 3
- 개발 로드맵 (Phase 1~3)

[4/5] 재무 모델 (목표 IRR: {target_irr})
- Unit Economics: ASP / CM% / LTV:CAC / Payback
- IRR 역산: 필요 Year-5 FCF $___M
- 3-시나리오: Bull/Base/Bear

[5/5] PE-3 검증 결과
- 점수: __/100
- 연계 권고: [PE-STRAT / PE-FIN / PE-SEMI / PE-AI]

📌 핵심 결론 (3문장)
🔗 연계 라이브러리 권고: [...]
=========================================== """


# ── PE-3-PROD QC 실행 헬퍼 ──────────────────────────────────────────────────

def run_pe3_qc(text: str, idea_name: str = "",
               strict: bool = False) -> dict:
    """
    GPT 출력 텍스트에 PE-3-PROD 체크리스트를 적용.
    반환: {"overall": float, "grade": str, "failed_must": [...], "raw": dict}
    """
    if not _QC_AVAILABLE:
        print("  ⚠️  [QC] pe3_product_validator 미임포트 — QC 건너뜀")
        return {"overall": None, "grade": "N/A", "failed_must": [], "raw": {}}

    # YAML 체크리스트 우선, 없으면 내장 폴백
    yaml_path = str(_CHECKLIST_YAML) if _CHECKLIST_YAML.exists() else None
    checks = load_checks(yaml_path)

    result = _qc_validate(text, checks)
    overall = result["overall"]
    grade   = result["grade"]

    # MUST 항목 중 미통과 목록
    failed_must = []
    for d_id, dr in result["dimensions"].items():
        for chk in dr["checks"]:
            if chk["level"] == "MUST" and not chk["passed"]:
                failed_must.append(f"{chk['id']}: {chk['name']}")

    # 콘솔 출력
    bar_filled = int(overall / 5) if overall else 0
    bar = "█" * bar_filled + "░" * (20 - bar_filled)
    print(f"  🔍 [PE-3 QC] [{bar}] {overall:.1f}%  {grade}")
    if failed_must:
        print(f"  ⚠️  MUST 미충족 ({len(failed_must)}건):")
        for item in failed_must:
            print(f"      ✘ {item}")
    else:
        print(f"  ✅ 모든 MUST 항목 통과")

    if strict and overall < 88:
        raise ValueError(
            f"[QC-STRICT] PE-3 점수 {overall:.1f}% < 88% "
            f"— '{idea_name}' Notion 업데이트 중단"
        )

    return {"overall": overall, "grade": grade,
            "failed_must": failed_must, "raw": result}


# ── Notion API 헬퍼 ──────────────────────────────────────────────────────────

def notion_query_pending(dry_run: bool = False) -> list[dict]:
    """MECE Status == '⏳ 대기중' 레코드 조회."""
    url = f"https://api.notion.com/v1/databases/{DB_ID}/query"
    payload = {
        "filter": {
            "property": "MECE Status",
            "select": {"equals": "⏳ 대기중"}
        },
        "sorts": [{"property": "Created", "direction": "ascending"}]
    }
    if dry_run:
        print("[DRY-RUN] Notion 쿼리 시뮬레이션 — 실제 API 미호출")
        return []
    resp = requests.post(url, headers=NOTION_HEADERS, json=payload, timeout=15)
    resp.raise_for_status()
    return resp.json().get("results", [])


def notion_update_status(page_id: str, status: str,
                         pe3_score: float = None,
                         irr_result: float = None,
                         tam: str = None,
                         key_insight: str = None,
                         draft_url: str = None,
                         cross_libs: list = None,
                         pe3_grade: str = None,
                         pe3_failed_must: list = None) -> None:
    """레코드 상태 및 분석 결과 필드 업데이트 (PE-3 QC 필드 포함)."""
    props = {
        "MECE Status": {"select": {"name": status}}
    }
    if pe3_score is not None:
        props["PE3 Score"] = {"number": pe3_score}
    if pe3_grade:
        # Notion에 Grade 텍스트 기록 (선택 필드 없을 경우 rich_text)
        props["PE3 Grade"] = {"rich_text": [{"text": {"content": pe3_grade[:100]}}]}
    if pe3_failed_must:
        failed_str = "\n".join(pe3_failed_must)[:2000]
        props["PE3 Failed Must"] = {"rich_text": [{"text": {"content": failed_str}}]}
    if irr_result is not None:
        props["IRR Result"] = {"number": irr_result}
    if tam:
        props["TAM"] = {"rich_text": [{"text": {"content": tam[:2000]}}]}
    if key_insight:
        props["Key Insight"] = {"rich_text": [{"text": {"content": key_insight[:2000]}}]}
    if draft_url:
        props["Notion Draft URL"] = {"url": draft_url}
    if cross_libs:
        props["Cross Library"] = {"multi_select": [{"name": lib} for lib in cross_libs]}

    url = f"https://api.notion.com/v1/pages/{page_id}"
    resp = requests.patch(url, headers=NOTION_HEADERS,
                          json={"properties": props}, timeout=15)
    resp.raise_for_status()


def notion_create_draft_page(parent_page_id: str, idea_name: str,
                              analysis_md: str, pe3_score: float = None,
                              pe3_grade: str = None) -> str:
    """분석 초안을 Notion 하위 페이지로 생성 후 URL 반환."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    grade_tag = f" [{pe3_grade.split('—')[0].strip()}]" if pe3_grade else ""
    score_tag = f" | PE-3: {pe3_score:.0f}점" if pe3_score is not None else ""
    payload = {
        "parent": {"page_id": parent_page_id},
        "properties": {
            "title": {
                "title": [{
                    "text": {
                        "content": f"[PE-PROD] {idea_name} 초안 {today}{grade_tag}{score_tag}"
                    }
                }]
            }
        },
        "children": [{
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": analysis_md[:2000]}}]
            }
        }]
    }
    resp = requests.post("https://api.notion.com/v1/pages",
                         headers=NOTION_HEADERS, json=payload, timeout=20)
    resp.raise_for_status()
    page_id = resp.json()["id"]
    return f"https://www.notion.so/{page_id.replace('-', '')}"


# ── OpenAI API 호출 ──────────────────────────────────────────────────────────

def call_openai(user_prompt: str, dry_run: bool = False) -> str:
    """gpt-4o로 PE-PROD-ORCH 분석 실행."""
    if dry_run:
        # dry-run: PE-3 QC 검증 가능한 최소 샘플 텍스트 반환
        return (
            "[DRY-RUN 시뮬레이션 출력]\n\n"
            "SYSTEM ROLE: 당신은 신사업 기획 전문가입니다.\n"
            "=" * 43 + "\n"
            "📦 DRY-RUN 아이디어 — PE-PROD 표준 분석 보고서\n"
            "[1/5] 점수: 0/100\n"
            "- Layer A (고객): B2B SaaS 기업\n"
            "- Layer B (문제): Pain Point — 시장 Gap 분석\n"
            "- Layer C (솔루션): Build / Buy / Partner\n"
            "- Layer D (수익): SaaS 구독 LTV:CAC = 3:1 Payback 18개월\n"
            "- Layer E (경쟁): 직접 경쟁 대체재 Moat\n"
            "TAM: $10B | SAM: $2B | SOM: $200M\n"
            "IRR: 22% 역산 NPV = 0\n"
            "Bull/Base Bear 3-시나리오\n"
            "리스크 매트릭스: Critical 대응 방안\n"
            "Executive Summary: 핵심 결론 3문장.\n"
            "[HIGH] 근거수준 PE-FIN PE-STRAT\n"
            "PE-PROD-ORCH 실행 명령어: ```javascript\nPE-PROD-01\n```\n"
            "[5/5] PE-3 검증 결과\n"
            "- 점수: 91/100\n"
            "📌 핵심 결론\n이것은 드라이런 시뮬레이션입니다.\n"
            "🔗 연계 라이브러리 권고: [PE-FIN, PE-STRAT]\n"
        )

    resp = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-4o",
            "temperature": 0.1,
            "max_tokens": 4000,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_prompt},
            ],
        },
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


# ── 분석 결과 파싱 ────────────────────────────────────────────────────────────

def parse_analysis(text: str) -> dict:
    """분석 텍스트에서 주요 수치 추출."""
    import re
    result = {"pe3_score": None, "irr": None, "tam": None,
              "key_insight": None, "cross_libs": []}

    m = re.search(r"점수[:\s]*([\d\.]+)/100", text)
    if m:
        result["pe3_score"] = float(m.group(1))

    m = re.search(r"IRR[:\s]*([\d\.]+)%", text)
    if m:
        result["irr"] = float(m.group(1))

    m = re.search(r"TAM[:\s]*\$([\d\.]+[BMT]?[^\n]*)", text)
    if m:
        result["tam"] = f"${m.group(1).strip()}"

    m = re.search(r"📌 핵심 결론.*?\n([^\n]+)", text, re.DOTALL)
    if m:
        result["key_insight"] = m.group(1).strip()

    for lib in ["PE-STRAT", "PE-FIN", "PE-SEMI", "PE-AI", "PE-DD"]:
        if lib in text:
            result["cross_libs"].append(lib)

    return result


# ── GitHub Issue 등록 ────────────────────────────────────────────────────────

def create_github_issue(idea_name: str, notion_url: str,
                        pe3_score: float, pe3_grade: str = "",
                        dry_run: bool = False) -> None:
    if not GITHUB_TOKEN or dry_run:
        return
    body = (
        f"**PE-PROD-ORCH 자동분석 완료**\n\n"
        f"- 아이디어: {idea_name}\n"
        f"- PE-3 점수: {pe3_score}/100  {pe3_grade}\n"
        f"- Notion 초안: {notion_url}\n\n"
        f"자동 생성 by PE-7 루프 v1.1 ({datetime.now().strftime('%Y-%m-%d %H:%M KST')})"
    )
    owner, repo = GH_REPO.split("/")
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    requests.post(
        url,
        headers={"Authorization": f"Bearer {GITHUB_TOKEN}",
                 "Accept": "application/vnd.github+json"},
        json={"title": f"[PE-PROD] {idea_name} 분석 완료",
              "body": body,
              "labels": ["PE-PROD", "auto-analysis"]},
        timeout=15,
    )


# ── 레코드 단건 처리 ─────────────────────────────────────────────────────────

def process_record(record: dict, dry_run: bool = False,
                   qc_strict: bool = False) -> dict:
    props    = record["properties"]
    page_id  = record["id"]
    today    = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    def get_select(key): return (props.get(key, {}).get("select") or {}).get("name", "범용")
    def get_title(key):  return "".join(t["plain_text"] for t in props.get(key, {}).get("title", []))

    idea_name  = get_title("Idea Name") or "(무제)"
    domain     = get_select("Domain")
    actor_type = get_select("Actor Type")
    depth      = get_select("Analysis Depth") or "Standard"
    target_irr = get_select("Target IRR") or "20%"

    print(f"\n🔍 처리 중: [{idea_name}] | {domain} | {depth} | IRR {target_irr}")

    # Step 1) 상태 → 분석중
    if not dry_run:
        notion_update_status(page_id, "🔄 분석중")

    # Step 2) 프롬프트 조합
    user_prompt = USER_PROMPT_TEMPLATE.format(
        idea_name=idea_name, actor_type=actor_type, domain=domain,
        depth=depth, target_irr=target_irr, today=today
    )

    # Step 3) OpenAI 호출
    try:
        analysis_text = call_openai(user_prompt, dry_run=dry_run)
    except Exception as e:
        print(f"  ❌ OpenAI 오류: {e}")
        if not dry_run:
            notion_update_status(page_id, "❌ 오류")
        return {"idea": idea_name, "status": "error", "error": str(e)}

    # Step 3.5) ★ PE-3-PROD QC 인라인 검증 ★
    qc_result = {"overall": None, "grade": "N/A", "failed_must": [], "raw": {}}
    try:
        qc_result = run_pe3_qc(analysis_text, idea_name=idea_name, strict=qc_strict)
    except ValueError as qc_err:
        # --qc-strict 모드에서 88점 미만 시 여기서 중단
        print(f"  🛑 {qc_err}")
        if not dry_run:
            notion_update_status(page_id, "🔄 QC 재검토 필요",
                                 pe3_score=qc_result.get("overall"),
                                 pe3_grade=qc_result.get("grade", ""),
                                 pe3_failed_must=qc_result.get("failed_must", []))
        return {"idea": idea_name, "status": "qc_fail",
                "qc": qc_result, "error": str(qc_err)}

    # Step 4) GPT 출력 파싱 (수치 추출)
    parsed = parse_analysis(analysis_text)

    # QC 실측 점수로 pe3_score 덮어쓰기 (GPT 자가채점보다 QC 실측 우선)
    if qc_result["overall"] is not None:
        parsed["pe3_score"] = round(qc_result["overall"], 1)

    # Step 5) Notion 초안 페이지 생성
    draft_url = ""
    if not dry_run:
        try:
            draft_url = notion_create_draft_page(
                page_id, idea_name, analysis_text,
                pe3_score=parsed["pe3_score"],
                pe3_grade=qc_result["grade"]
            )
            print(f"  📄 초안 페이지: {draft_url}")
        except Exception as e:
            print(f"  ⚠️  초안 페이지 생성 실패: {e}")

    # Step 6) DB 레코드 최종 업데이트 (PE3 Score + PE3 Grade + PE3 Failed Must)
    if not dry_run:
        notion_update_status(
            page_id, "✅ 완료",
            pe3_score=parsed["pe3_score"],
            pe3_grade=qc_result["grade"],
            pe3_failed_must=qc_result["failed_must"],
            irr_result=parsed["irr"],
            tam=parsed["tam"],
            key_insight=parsed["key_insight"],
            draft_url=draft_url,
            cross_libs=parsed["cross_libs"],
        )

    # Step 7) GitHub Issue 등록
    create_github_issue(idea_name, draft_url,
                        parsed["pe3_score"] or 0,
                        pe3_grade=qc_result["grade"],
                        dry_run=dry_run)

    print(f"  ✅ 완료 | PE-3: {parsed['pe3_score']} ({qc_result['grade']}) "
          f"| IRR: {parsed['irr']}%")
    return {"idea": idea_name, "status": "done",
            "parsed": parsed, "qc": qc_result}


# ── --qc-only 모드: 로컬 파일 QC 단독 실행 ──────────────────────────────────

def qc_only_mode(file_path: str, strict: bool = False) -> int:
    """
    API 호출 없이 로컬 .md 파일에 PE-3-PROD QC만 실행.
    테스트/디버깅용.
    """
    if not _QC_AVAILABLE:
        print("❌ pe3_product_validator 모듈 없음")
        return 1
    content = Path(file_path).read_text(encoding="utf-8")
    print(f"\n🔬 QC-Only Mode — {Path(file_path).name}")
    qc = run_pe3_qc(content, idea_name=Path(file_path).stem, strict=strict)

    print("\n  차원별 상세:")
    sep = "─" * 56
    print(f"  {sep}")
    for d_id, dr in sorted(qc["raw"].get("dimensions", {}).items()):
        bar = "█" * int(dr["pct"] / 5) + "░" * (20 - int(dr["pct"] / 5))
        print(f"  {d_id} {dr['name']}")
        print(f"  [{bar}] {dr['pct']}%")
        for chk in dr["checks"]:
            icon = "✔" if chk["passed"] else "✘"
            print(f"    {icon} [{chk['level']:<6}] {chk['id']}: {chk['name']}")
    print(f"  {sep}")
    print(f"  Overall : {qc['overall']:.1f}%  {qc['grade']}")
    print(f"  {sep}\n")
    return 0 if (not strict or qc["overall"] >= 88) else 1


# ── 메인 폴링 루프 ────────────────────────────────────────────────────────────

def run_once(dry_run: bool = False, record_id: str = None,
             qc_strict: bool = False) -> list[dict]:
    results = []
    if record_id:
        url  = f"https://api.notion.com/v1/pages/{record_id}"
        resp = requests.get(url, headers=NOTION_HEADERS, timeout=15)
        resp.raise_for_status()
        records = [resp.json()]
    else:
        records = notion_query_pending(dry_run=dry_run)

    if not records:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 대기 중인 아이디어 없음")
        return []

    print(f"[{datetime.now().strftime('%H:%M:%S')}] {len(records)}건 감지")
    for rec in records:
        res = process_record(rec, dry_run=dry_run, qc_strict=qc_strict)
        results.append(res)
        time.sleep(2)
    return results


def main():
    parser = argparse.ArgumentParser(
        description="PE-7 Product Idea → MECE 자동분석 루프 v1.1"
    )
    parser.add_argument("--watch",      action="store_true", help="반복 폴링 모드")
    parser.add_argument("--dry-run",    action="store_true",
                        help="Notion/OpenAI API 미호출, QC 로직은 실행")
    parser.add_argument("--qc-only",    action="store_true",
                        help="로컬 파일 QC 단독 실행 (--file 필요)")
    parser.add_argument("--file",       help="--qc-only 대상 파일 경로")
    parser.add_argument("--qc-strict",  action="store_true",
                        help="88점 미만 시 Notion 업데이트 중단")
    parser.add_argument("--record-id",  help="특정 Notion 페이지 ID만 처리")
    parser.add_argument("--output",     help="결과 JSON 저장 경로")
    args = parser.parse_args()

    # ── qc-only 모드 (API 불필요) ──
    if args.qc_only:
        if not args.file:
            print("❌ --qc-only 모드에는 --file 경로가 필요합니다")
            sys.exit(1)
        sys.exit(qc_only_mode(args.file, strict=args.qc_strict))

    if not NOTION_TOKEN and not args.dry_run:
        print("❌ NOTION_TOKEN 환경변수 미설정"); sys.exit(1)
    if not OPENAI_KEY and not args.dry_run:
        print("❌ OPENAI_API_KEY 환경변수 미설정"); sys.exit(1)

    qc_status = "✅ 활성" if _QC_AVAILABLE else "⚠️ 미임포트 (QC 건너뜀)"
    print("🚀 PE-7 Product Idea → MECE 자동분석 루프 v1.1 시작")
    print(f"   DB ID      : {DB_ID}")
    print(f"   Dry-Run    : {args.dry_run}")
    print(f"   Watch 모드 : {args.watch}")
    print(f"   PE-3 QC    : {qc_status}")
    print(f"   QC Strict  : {args.qc_strict}")

    all_results = []
    try:
        if args.watch:
            while True:
                results = run_once(dry_run=args.dry_run,
                                   record_id=args.record_id,
                                   qc_strict=args.qc_strict)
                all_results.extend(results)
                print(f"  ⏱  {POLL_INTERVAL}초 후 재폴링...")
                time.sleep(POLL_INTERVAL)
        else:
            all_results = run_once(dry_run=args.dry_run,
                                   record_id=args.record_id,
                                   qc_strict=args.qc_strict)
    except KeyboardInterrupt:
        print("\n🛑 루프 중단")

    if args.output and all_results:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)
        print(f"📄 결과 저장: {args.output}")

    failed = [r for r in all_results
              if r.get("status") in ("error", "qc_fail")]
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
