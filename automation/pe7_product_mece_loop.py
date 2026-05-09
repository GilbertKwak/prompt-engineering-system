#!/usr/bin/env python3
"""
pe7_product_mece_loop.py — PE-7 Product Idea → MECE 자동분석 루프
Version : 2.0 | Date: 2026-05-09
Author  : Gilbert

Changelog v2.0:
  [★ CORE] D6/D7/D8 파싱 패턴 신규 추가
    - D6: IRR 역산 (Entry EV 상한선·Exit Multiple 감응도·Bear IRR)
    - D7: Blue Ocean ERRC 4액션 + North Star Metric + Vanity Metric 경고
    - D8: KPI 로드맵 (Phase 마일스톤·핵심 KPI·Go/No-Go 트리거)
  [★ NOTION] D6/D7/D8 신규 필드 Notion 자동 기록
  [★ FLAGS] --pe3-dashboard / --revalidate-all / --ab-test 플래그 추가
  [★ DRY-RUN] 샘플 텍스트에 D6~D8 섹션 포함 (QC 실측 가능)
  [FIX] parse_analysis 반환 키 v2 표준화
  [FIX] cross_libs에 PE-NBD, PE-STRAT 추가

Changelog v1.1 (이전):
  - pe3_product_validator.validate() 인라인 통합 (Step 3.5)
  - QC 점수 → Notion PE3 Score 자동 기록
  - --dry-run / --qc-only / --qc-strict 플래그

Pipeline v2.0:
  Notion DB 폴링
    → '⏳ 대기중' 레코드 감지
    → PE-PROD-ORCH v2 프롬프트 조합 (9-Framework)
    → OpenAI API 호출 (gpt-4o)
    → PE-3-PROD QC 자동 검증 (D1~D8)
    → D6/D7/D8 수치 파싱 & Notion 기록
    → 분석 초안 Notion 하위 페이지 생성
    → DB 레코드 업데이트 (전체 필드)
    → GitHub Issue 등록 (선택)

Usage:
  python pe7_product_mece_loop.py                          # 폴링 1회
  python pe7_product_mece_loop.py --watch                  # 60초 반복
  python pe7_product_mece_loop.py --dry-run                # API 미호출
  python pe7_product_mece_loop.py --qc-only --file <f.md> # 로컬 QC
  python pe7_product_mece_loop.py --qc-strict              # 88점 미만 중단
  python pe7_product_mece_loop.py --record-id <id>         # 단건 처리
  python pe7_product_mece_loop.py --revalidate-all         # 전체 Notion QC 재검증
  python pe7_product_mece_loop.py --pe3-dashboard          # PE-3 점수 대시보드
  python pe7_product_mece_loop.py --ab-test \              # v1 vs v2 A/B 비교
    --v1 pe_prod_orch_v1.md --v2 pe_prod_orch_v2.md

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
    _this_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(_this_dir))
    from pe3_product_validator import validate as _qc_validate, BUILTIN_CHECKS, load_checks
    _QC_AVAILABLE = True
except ImportError:
    pass


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

_CHECKLIST_YAML = Path(__file__).resolve().parent.parent / "config" / "pe3_product_checklist.yaml"


# ── MECE 분석 프롬프트 (PE-PROD-ORCH v2.0 · 9-Framework) ─────────────────────
SYSTEM_PROMPT = """당신은 McKinsey/BCG급 신사업 기획 전문가이자 MECE 분석 AI입니다.
PE-PROD-ORCH v2.0 파이프라인을 실행합니다 (9-Framework: 3C|Porter5|SWOT|JTBD|AARRR|BlueOcean|LeanCanvas|NSM|LogicTree).
Temperature: 0.1 (구조 설계) | 출력 포맷은 반드시 아래 표준 템플릿을 따릅니다."""

USER_PROMPT_TEMPLATE = """PE-PROD-ORCH v2.0 전체 파이프라인을 실행해줘.

분석 대상  : {idea_name}
주체 유형  : {actor_type}
도메인     : {domain}
분석 깊이  : {depth}
목표 IRR   : {target_irr}
Entry EV   : {entry_ev}
PE-FIN 연동: Yes

---

## 출력 표준 포맷 v2.0 (MECE 8-Block 반드시 준수)

===========================================
📦 {idea_name} — PE-PROD v2.0 분석 보고서
분석일: {today} | 버전: v2.0
===========================================

## B1. 문제 정의 & 3C 분석
- Company 핵심역량:
- Customer 핵심고객·Pain Point·이탈원인:
- Competitor 직접·간접·대체재:

## B2. 시장구조 & Porter 5 Forces
- TAM: $___B | SAM: $___B | SOM: $___M | CAGR: ___%
- Porter 5 Forces: [기존경쟁/신규진입/공급자/구매자/대체재] = [H/M/L]

## B3. 고객심리 & JTBD
- Functional Jobs (3개):
- Emotional Jobs (2개):
- Social Jobs (1개):
- Switching Trigger (2개):

## B4. 성장퍼널 & AARRR
- Acquisition: Top3 채널 | CAC 가정 $___ 
- Activation: 온보딩 병목 | 첫경험 KPI
- Retention: 락인요소 | 이탈원인
- Revenue: ARPU $__ | 결제전환율 __%
- Referral: 바이럴 메커니즘 | NPS 목표

## B5. 비즈니스 모델 & Lean Canvas
- 수익모델 유형:
- 단가구조:
- Unit Economics: CAC $__ | LTV $__ | Payback __개월
- Unique Value Proposition:
- Unfair Advantage:

## B6. 재무 시나리오 & IRR 역산
- 3-시나리오 매출: Bull $__M | Base $__M | Bear $__M (Year-3)
- IRR 역산: Entry EV={entry_ev}억 기준 IRR ≈ __%
- IRR 목표 달성 Entry EV 상한선: ___억원
- Exit Multiple ±1x → IRR 변화폭: +/-__%
- Bear IRR: __%
- 재무 리스크 Top 3: [확률·영향도]

## B7. Blue Ocean & North Star Metric
- ERRC: Eliminate(_) | Reduce(_) | Raise(_) | Create(_)
- 신규시장 창출 가능성:
- North Star Metric: [지표명 | 측정주기 | 목표값]
- NSM 선행지표 3개:
- Vanity Metric 경고:

## B8. 실행 로드맵 & KPI
- Phase 1 (0~6개월) 마일스톤:
- Phase 2 (6~18개월) 마일스톤:
- Phase 3 (18~36개월) 마일스톤:
- 핵심 KPI 5개: [지표|측정주기|목표값]
- Go/No-Go 트리거:

## Strategic Priorities
| Priority | Strategy | Impact | Difficulty | Time Horizon |
|---|---|---|---|---|

## Top 5 Key Insights
1.
2.
3.
4.
5.

## PE-3 검증 결과
- 점수: __/100
- 연계 권고: [PE-FIN | PE-STRAT | PE-SEMI | PE-NBD | PE-DD]

📌 핵심 결론 (3문장)
🔗 연계 라이브러리 권고: [...]
=========================================== """


# ── PE-3-PROD QC ─────────────────────────────────────────────────────────────

def run_pe3_qc(text: str, idea_name: str = "",
               strict: bool = False) -> dict:
    if not _QC_AVAILABLE:
        print("  ⚠️  [QC] pe3_product_validator 미임포트 — QC 건너뜀")
        return {"overall": None, "grade": "N/A", "failed_must": [], "raw": {}}

    yaml_path = str(_CHECKLIST_YAML) if _CHECKLIST_YAML.exists() else None
    checks = load_checks(yaml_path)
    result = _qc_validate(text, checks)
    overall = result["overall"]
    grade   = result["grade"]

    failed_must = []
    for d_id, dr in result["dimensions"].items():
        for chk in dr["checks"]:
            if chk["level"] == "MUST" and not chk["passed"]:
                failed_must.append(f"{chk['id']}: {chk['name']}")

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

def notion_query_pending(dry_run: bool = False) -> list:
    url = f"https://api.notion.com/v1/databases/{DB_ID}/query"
    payload = {
        "filter": {
            "property": "MECE Status",
            "select": {"equals": "⏳ 대기중"}
        },
        "sorts": [{"property": "Created", "direction": "ascending"}]
    }
    if dry_run:
        print("[DRY-RUN] Notion 쿼리 시뮬레이션")
        return []
    resp = requests.post(url, headers=NOTION_HEADERS, json=payload, timeout=15)
    resp.raise_for_status()
    return resp.json().get("results", [])


def notion_query_all_completed() -> list:
    """--revalidate-all용: 완료 레코드 전체 조회."""
    url = f"https://api.notion.com/v1/databases/{DB_ID}/query"
    payload = {
        "filter": {
            "property": "MECE Status",
            "select": {"equals": "✅ 완료"}
        }
    }
    all_records = []
    while True:
        resp = requests.post(url, headers=NOTION_HEADERS, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        all_records.extend(data.get("results", []))
        if not data.get("has_more"):
            break
        payload["start_cursor"] = data["next_cursor"]
    return all_records


def notion_update_status(
    page_id: str, status: str,
    pe3_score: float = None,
    pe3_grade: str = None,
    pe3_failed_must: list = None,
    irr_result: float = None,
    irr_entry_ev_cap: str = None,
    irr_bear: float = None,
    irr_exit_sensitivity: str = None,
    tam: str = None,
    key_insight: str = None,
    draft_url: str = None,
    cross_libs: list = None,
    # ── D7 신규 ──
    nsm_metric: str = None,
    nsm_target: str = None,
    blue_ocean_score: str = None,
    vanity_metric_warning: str = None,
    # ── D8 신규 ──
    kpi_phase1: str = None,
    kpi_phase2: str = None,
    kpi_phase3: str = None,
    go_no_go_trigger: str = None,
) -> None:
    """레코드 상태 및 D6/D7/D8 분석 결과 필드 업데이트."""

    def rt(val, limit=2000):
        """Notion rich_text 블록 생성 헬퍼."""
        return {"rich_text": [{"text": {"content": str(val)[:limit]}}]}

    props = {"MECE Status": {"select": {"name": status}}}

    # ── 기존 필드 (D1~D5) ──
    if pe3_score is not None:
        props["PE3 Score"]       = {"number": pe3_score}
    if pe3_grade:
        props["PE3 Grade"]       = rt(pe3_grade)
    if pe3_failed_must:
        props["PE3 Failed Must"] = rt("\n".join(pe3_failed_must))
    if irr_result is not None:
        props["IRR Result"]      = {"number": irr_result}
    if tam:
        props["TAM"]             = rt(tam)
    if key_insight:
        props["Key Insight"]     = rt(key_insight)
    if draft_url:
        props["Notion Draft URL"] = {"url": draft_url}
    if cross_libs:
        props["Cross Library"]   = {"multi_select": [{"name": l} for l in cross_libs]}

    # ── D6 신규 필드: IRR 역산 세부 ──
    if irr_entry_ev_cap:
        props["IRR Entry EV Cap"]      = rt(irr_entry_ev_cap)
    if irr_bear is not None:
        props["IRR Bear"]               = {"number": irr_bear}
    if irr_exit_sensitivity:
        props["IRR Exit Sensitivity"]   = rt(irr_exit_sensitivity)

    # ── D7 신규 필드: Blue Ocean & NSM ──
    if nsm_metric:
        props["NSM Metric"]             = rt(nsm_metric)
    if nsm_target:
        props["NSM Target"]             = rt(nsm_target)
    if blue_ocean_score:
        props["Blue Ocean Score"]       = rt(blue_ocean_score)
    if vanity_metric_warning:
        props["Vanity Metric Warning"]  = rt(vanity_metric_warning)

    # ── D8 신규 필드: KPI 로드맵 ──
    if kpi_phase1:
        props["KPI Phase1"]             = rt(kpi_phase1)
    if kpi_phase2:
        props["KPI Phase2"]             = rt(kpi_phase2)
    if kpi_phase3:
        props["KPI Phase3"]             = rt(kpi_phase3)
    if go_no_go_trigger:
        props["Go No-Go Trigger"]       = rt(go_no_go_trigger)

    url = f"https://api.notion.com/v1/pages/{page_id}"
    resp = requests.patch(url, headers=NOTION_HEADERS,
                          json={"properties": props}, timeout=15)
    resp.raise_for_status()


def notion_create_draft_page(parent_page_id: str, idea_name: str,
                              analysis_md: str, pe3_score: float = None,
                              pe3_grade: str = None) -> str:
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
    if dry_run:
        # D6~D8 섹션 포함 (QC 실측 가능 샘플)
        return (
            "[DRY-RUN v2.0 시뮬레이션 출력]\n\n"
            "## B1. 문제 정의 & 3C 분석\n"
            "- Company 핵심역량: AI 반도체 설계 IP\n"
            "- Customer 핵심고객: Fabless HPC 스타트업 Pain Point — 설계 사이클 12개월 이탈원인 — 비용\n"
            "- Competitor 직접: Arm IP 간접: RISC-V 대체재: FPGA 프로토타이핑\n\n"
            "## B2. 시장구조 & Porter 5 Forces\n"
            "- TAM: $45B | SAM: $8B | SOM: $400M | CAGR: 18%\n"
            "- Porter 5 Forces: [기존경쟁 H / 신규진입 M / 공급자 H / 구매자 M / 대체재 L]\n\n"
            "## B3. 고객심리 & JTBD\n"
            "- Functional Jobs: 설계기간 단축 | 수율 예측 | 테이프아웃 비용 절감\n"
            "- Emotional Jobs: 기술 우위 확신 | 실패 불안 해소\n"
            "- Social Jobs: CTO 포트폴리오 강화\n"
            "- Switching Trigger: 기존 EDA 라이선스 갱신 시점 | 투자 라운드 후 스케일업\n\n"
            "## B4. 성장퍼널 & AARRR\n"
            "- Acquisition: 반도체 학회 | LinkedIn 타겟광고 | 파트너 추천 CAC $2,800\n"
            "- Activation: POC 완료율 >60% 병목: 계약 심사\n"
            "- Retention: IP 갱신 계약 | 기술지원 SLA 이탈원인: 경쟁사 가격\n"
            "- Revenue: ARPU $180K | 결제전환율 32%\n"
            "- Referral: 고객사 CTO 추천 네트워크 NPS 목표 55+\n\n"
            "## B5. 비즈니스 모델 & Lean Canvas\n"
            "- 수익모델: 라이선스 + 로열티 하이브리드\n"
            "- 단가구조: Basic $50K | Pro $180K | Enterprise $500K+\n"
            "- Unit Economics: CAC $2,800 | LTV $540K | Payback 6개월\n"
            "- UVP: 설계 사이클 40% 단축 & 수율 +8%p\n"
            "- Unfair Advantage: 독자 EDA 알고리즘 특허 3건\n\n"
            "## B6. 재무 시나리오 & IRR 역산\n"
            "- 3-시나리오: Bull $120M | Base $80M | Bear $40M (Year-3)\n"
            "- IRR 역산: Entry EV=500억 기준 IRR ≈ 28%\n"
            "- IRR 목표 달성 Entry EV 상한선: 650억원\n"
            "- Exit Multiple ±1x → IRR 변화폭: +/-4.2%\n"
            "- Bear IRR: 14%\n"
            "- 재무 리스크: 고객집중(확률 H·영향 H) | FX(M·M) | 특허분쟁(L·H)\n\n"
            "## B7. Blue Ocean & North Star Metric\n"
            "- ERRC: Eliminate(EDA 고정비) | Reduce(설계기간) | Raise(수율예측정확도) | Create(AI-in-loop 자동검증)\n"
            "- 신규시장: AI-HW Co-design Platform (경쟁 없음)\n"
            "- North Star Metric: 고객사 테이프아웃 성공률 | 월별 | 목표 85%\n"
            "- NSM 선행지표: POC 완료율 | 설계반복횟수 | SLA 응답시간\n"
            "- Vanity Metric 경고: 다운로드 수·페이지뷰는 수익 무관\n\n"
            "## B8. 실행 로드맵 & KPI\n"
            "- Phase 1 (0~6개월): POC 고객 3사 계약 | IP v1 릴리즈\n"
            "- Phase 2 (6~18개월): ARR $5M 달성 | 파트너 2개\n"
            "- Phase 3 (18~36개월): Series B | ARR $20M | 해외 진출\n"
            "- 핵심 KPI: ARR|월|$20M / NPS|분기|55+ / 수율|월|85% / CAC|분기|<$3K / Churn|월|<5%\n"
            "- Go/No-Go 트리거: 6개월 ARR < $1M → Pivot 검토\n\n"
            "## PE-3 검증 결과\n"
            "- 점수: 93/100\n"
            "📌 핵심 결론\nAI 반도체 설계 IP 플랫폼은 TAM $45B 시장에서 경쟁 없는 포지션을 확보할 수 있습니다.\n"
            "🔗 연계 라이브러리 권고: [PE-FIN, PE-SEMI, PE-STRAT, PE-NBD]\n"
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
            "max_tokens": 6000,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_prompt},
            ],
        },
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


# ── 분석 결과 파싱 v2.0 (D6/D7/D8 추가) ─────────────────────────────────────

def parse_analysis(text: str) -> dict:
    """
    GPT 분석 텍스트에서 D1~D8 전 차원 수치 추출.

    반환 키:
      D1~D5 (기존): pe3_score, irr, tam, key_insight, cross_libs
      D6 (신규): irr_entry_ev_cap, irr_bear, irr_exit_sensitivity
      D7 (신규): nsm_metric, nsm_target, blue_ocean_actions, vanity_metric_warning
      D8 (신규): kpi_phase1, kpi_phase2, kpi_phase3, go_no_go_trigger
    """
    import re

    result = {
        # D1~D5
        "pe3_score":           None,
        "irr":                 None,
        "tam":                 None,
        "key_insight":         None,
        "cross_libs":          [],
        # D6: IRR 역산 세부
        "irr_entry_ev_cap":    None,   # Entry EV 상한선
        "irr_bear":            None,   # Bear 시나리오 IRR
        "irr_exit_sensitivity": None,  # Exit Multiple 감응도
        # D7: Blue Ocean & NSM
        "nsm_metric":          None,   # North Star Metric 지표명
        "nsm_target":          None,   # NSM 목표값
        "blue_ocean_actions":  None,   # ERRC 요약
        "vanity_metric_warning": None, # Vanity Metric 경고 항목
        # D8: KPI 로드맵
        "kpi_phase1":          None,   # Phase 1 마일스톤
        "kpi_phase2":          None,   # Phase 2 마일스톤
        "kpi_phase3":          None,   # Phase 3 마일스톤
        "go_no_go_trigger":    None,   # Go/No-Go 트리거
    }

    # ── D1~D5 파싱 (기존) ────────────────────────────────────────────────────
    m = re.search(r"점수[:\s]*([\d\.]+)/100", text)
    if m:
        result["pe3_score"] = float(m.group(1))

    m = re.search(r"IRR[\s\u00a0]*(?:역산|결과|기준)[^\n]*?([\d\.]+)%", text)
    if m:
        result["irr"] = float(m.group(1))
    elif (m := re.search(r"IRR\s*[≈=~]\s*([\d\.]+)%", text)):
        result["irr"] = float(m.group(1))

    m = re.search(r"TAM[:\s]*\$([\d\.]+[BMT]?[^\n]*)", text)
    if m:
        result["tam"] = f"${m.group(1).strip()}"

    m = re.search(r"📌 핵심 결론.*?\n([^\n]+)", text, re.DOTALL)
    if m:
        result["key_insight"] = m.group(1).strip()

    for lib in ["PE-STRAT", "PE-FIN", "PE-SEMI", "PE-AI", "PE-DD",
                "PE-NBD", "PE-CON", "PE-JV"]:
        if lib in text:
            result["cross_libs"].append(lib)

    # ── D6: IRR 역산 세부 파싱 ★ 신규 ─────────────────────────────────────
    # D6-1: Entry EV 상한선
    m = re.search(
        r"(?:Entry EV\s*상한선|IRR.*?Entry EV.*?상한)[^\d]*(\d[\d,\.]+)\s*억",
        text, re.IGNORECASE
    )
    if m:
        result["irr_entry_ev_cap"] = f"{m.group(1).replace(',', '')}억원"

    # D6-2: Bear IRR
    m = re.search(
        r"Bear\s*IRR[:\s]*([\d\.]+)%|Bear[^\n]*IRR[^\d]*([\d\.]+)%",
        text, re.IGNORECASE
    )
    if m:
        val = m.group(1) or m.group(2)
        result["irr_bear"] = float(val)

    # D6-3: Exit Multiple 감응도
    m = re.search(
        r"Exit\s*Multiple[^\n]*±\s*1x[^\n]*([\+\-][\d\.]+%[^\n]*)",
        text, re.IGNORECASE
    )
    if m:
        result["irr_exit_sensitivity"] = m.group(1).strip()
    else:
        m = re.search(
            r"Exit[^\n]*감응도[^\n]*([\d\.]+%[^\n]*)",
            text, re.IGNORECASE
        )
        if m:
            result["irr_exit_sensitivity"] = m.group(1).strip()

    # ── D7: Blue Ocean & North Star Metric 파싱 ★ 신규 ────────────────────
    # D7-1: North Star Metric 지표명
    m = re.search(
        r"North\s*Star\s*Metric[:\s]+([^\|\n]+)(?:\|([^\|\n]+))?(?:\|([^\n]+))?",
        text, re.IGNORECASE
    )
    if m:
        result["nsm_metric"] = m.group(1).strip()
        if m.group(3):
            result["nsm_target"] = m.group(3).strip()

    # D7-2: ERRC 4액션 한 줄 요약
    m = re.search(
        r"ERRC[:\s]+Eliminate\(([^)]+)\)[^R]*Reduce\(([^)]+)\)[^R]*Raise\(([^)]+)\)[^C]*Create\(([^)]+)\)",
        text, re.IGNORECASE | re.DOTALL
    )
    if m:
        result["blue_ocean_actions"] = (
            f"E:{m.group(1).strip()} | R:{m.group(2).strip()} "
            f"| R:{m.group(3).strip()} | C:{m.group(4).strip()}"
        )

    # D7-3: Vanity Metric 경고 항목
    m = re.search(
        r"Vanity\s*Metric\s*경고[:\s]+([^\n]+)",
        text, re.IGNORECASE
    )
    if m:
        result["vanity_metric_warning"] = m.group(1).strip()

    # ── D8: KPI 로드맵 파싱 ★ 신규 ──────────────────────────────────────────
    # D8-1: Phase 1 마일스톤
    m = re.search(
        r"Phase\s*1[^:\n]*:[\s]*([^\n]+(?:\|[^\n]+)?)",
        text, re.IGNORECASE
    )
    if m:
        result["kpi_phase1"] = m.group(1).strip()

    # D8-2: Phase 2 마일스톤
    m = re.search(
        r"Phase\s*2[^:\n]*:[\s]*([^\n]+(?:\|[^\n]+)?)",
        text, re.IGNORECASE
    )
    if m:
        result["kpi_phase2"] = m.group(1).strip()

    # D8-3: Phase 3 마일스톤
    m = re.search(
        r"Phase\s*3[^:\n]*:[\s]*([^\n]+(?:\|[^\n]+)?)",
        text, re.IGNORECASE
    )
    if m:
        result["kpi_phase3"] = m.group(1).strip()

    # D8-4: Go/No-Go 트리거
    m = re.search(
        r"Go[/\\]?No[\-\s]?Go\s*트리거[:\s]+([^\n]+)",
        text, re.IGNORECASE
    )
    if m:
        result["go_no_go_trigger"] = m.group(1).strip()

    return result


# ── GitHub Issue 등록 ────────────────────────────────────────────────────────

def create_github_issue(idea_name: str, notion_url: str,
                        pe3_score: float, pe3_grade: str = "",
                        parsed: dict = None,
                        dry_run: bool = False) -> None:
    if not GITHUB_TOKEN or dry_run:
        return
    d6_summary = ""
    d7_summary = ""
    d8_summary = ""
    if parsed:
        d6_summary = (
            f"\n- IRR (Base): {parsed.get('irr', 'N/A')}%  "
            f"Bear: {parsed.get('irr_bear', 'N/A')}%  "
            f"EV 상한: {parsed.get('irr_entry_ev_cap', 'N/A')}"
        )
        d7_summary = (
            f"\n- NSM: {parsed.get('nsm_metric', 'N/A')} → 목표 {parsed.get('nsm_target', 'N/A')}"
        )
        d8_summary = (
            f"\n- KPI Phase1: {parsed.get('kpi_phase1', 'N/A')}"
            f"\n- Go/No-Go: {parsed.get('go_no_go_trigger', 'N/A')}"
        )
    body = (
        f"**PE-PROD-ORCH v2.0 자동분석 완료**\n\n"
        f"- 아이디어: {idea_name}\n"
        f"- PE-3 점수: {pe3_score}/100  {pe3_grade}\n"
        f"- Notion 초안: {notion_url}\n"
        f"{d6_summary}{d7_summary}{d8_summary}\n\n"
        f"자동 생성 by PE-7 루프 v2.0 ({datetime.now().strftime('%Y-%m-%d %H:%M KST')})"
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
    def get_rt(key):     return "".join(t["plain_text"] for t in props.get(key, {}).get("rich_text", []))

    idea_name  = get_title("Idea Name") or "(무제)"
    domain     = get_select("Domain")
    actor_type = get_select("Actor Type")
    depth      = get_select("Analysis Depth") or "Standard"
    target_irr = get_select("Target IRR") or "20%"
    entry_ev   = get_rt("Entry EV") or "500"

    print(f"\n🔍 처리 중: [{idea_name}] | {domain} | {depth} | IRR {target_irr} | EV {entry_ev}억")

    if not dry_run:
        notion_update_status(page_id, "🔄 분석중")

    user_prompt = USER_PROMPT_TEMPLATE.format(
        idea_name=idea_name, actor_type=actor_type, domain=domain,
        depth=depth, target_irr=target_irr, entry_ev=entry_ev, today=today
    )

    try:
        analysis_text = call_openai(user_prompt, dry_run=dry_run)
    except Exception as e:
        print(f"  ❌ OpenAI 오류: {e}")
        if not dry_run:
            notion_update_status(page_id, "❌ 오류")
        return {"idea": idea_name, "status": "error", "error": str(e)}

    # Step 3.5) PE-3 QC
    qc_result = {"overall": None, "grade": "N/A", "failed_must": [], "raw": {}}
    try:
        qc_result = run_pe3_qc(analysis_text, idea_name=idea_name, strict=qc_strict)
    except ValueError as qc_err:
        print(f"  🛑 {qc_err}")
        if not dry_run:
            notion_update_status(page_id, "🔄 QC 재검토 필요",
                                 pe3_score=qc_result.get("overall"),
                                 pe3_grade=qc_result.get("grade", ""),
                                 pe3_failed_must=qc_result.get("failed_must", []))
        return {"idea": idea_name, "status": "qc_fail",
                "qc": qc_result, "error": str(qc_err)}

    # Step 4) D1~D8 전 차원 파싱
    parsed = parse_analysis(analysis_text)

    # QC 실측 점수 우선
    if qc_result["overall"] is not None:
        parsed["pe3_score"] = round(qc_result["overall"], 1)

    # Step 5) Notion 초안 페이지
    draft_url = ""
    if not dry_run:
        try:
            draft_url = notion_create_draft_page(
                page_id, idea_name, analysis_text,
                pe3_score=parsed["pe3_score"],
                pe3_grade=qc_result["grade"]
            )
            print(f"  📄 초안: {draft_url}")
        except Exception as e:
            print(f"  ⚠️  초안 페이지 생성 실패: {e}")

    # Step 6) Notion DB 전체 업데이트 (D6/D7/D8 포함)
    if not dry_run:
        notion_update_status(
            page_id, "✅ 완료",
            pe3_score=parsed["pe3_score"],
            pe3_grade=qc_result["grade"],
            pe3_failed_must=qc_result["failed_must"],
            irr_result=parsed["irr"],
            irr_entry_ev_cap=parsed["irr_entry_ev_cap"],
            irr_bear=parsed["irr_bear"],
            irr_exit_sensitivity=parsed["irr_exit_sensitivity"],
            tam=parsed["tam"],
            key_insight=parsed["key_insight"],
            draft_url=draft_url,
            cross_libs=parsed["cross_libs"],
            nsm_metric=parsed["nsm_metric"],
            nsm_target=parsed["nsm_target"],
            blue_ocean_score=parsed["blue_ocean_actions"],
            vanity_metric_warning=parsed["vanity_metric_warning"],
            kpi_phase1=parsed["kpi_phase1"],
            kpi_phase2=parsed["kpi_phase2"],
            kpi_phase3=parsed["kpi_phase3"],
            go_no_go_trigger=parsed["go_no_go_trigger"],
        )

    # Step 7) GitHub Issue (D6~D8 요약 포함)
    create_github_issue(idea_name, draft_url,
                        parsed["pe3_score"] or 0,
                        pe3_grade=qc_result["grade"],
                        parsed=parsed,
                        dry_run=dry_run)

    print(f"  ✅ 완료 | PE-3: {parsed['pe3_score']} ({qc_result['grade']}) "
          f"| IRR Base: {parsed['irr']}% Bear: {parsed['irr_bear']}% "
          f"| EV 상한: {parsed['irr_entry_ev_cap']} "
          f"| NSM: {parsed['nsm_metric']}")
    return {"idea": idea_name, "status": "done",
            "parsed": parsed, "qc": qc_result}


# ── --qc-only 모드 ────────────────────────────────────────────────────────────

def qc_only_mode(file_path: str, strict: bool = False) -> int:
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


# ── --revalidate-all 모드 ─────────────────────────────────────────────────────

def revalidate_all_mode(strict: bool = False) -> int:
    """
    Notion '✅ 완료' 레코드 전체를 대상으로
    기존 초안 페이지 내용을 다시 QC 검증하고 PE3 Score 갱신.
    """
    print("\n🔄 [revalidate-all] 전체 완료 레코드 QC 재검증 시작...")
    records = notion_query_all_completed()
    print(f"   대상 레코드: {len(records)}건")
    fail_count = 0
    for rec in records:
        page_id   = rec["id"]
        props     = rec["properties"]
        idea_name = "".join(
            t["plain_text"] for t in props.get("Idea Name", {}).get("title", [])
        ) or page_id[:8]

        # 기존 초안 URL에서 텍스트 재취득은 비용이 크므로
        # Key Insight + TAM 텍스트를 이어 붙여 최소 QC 수행
        key_insight = "".join(
            t["plain_text"]
            for t in props.get("Key Insight", {}).get("rich_text", [])
        )
        tam = "".join(
            t["plain_text"]
            for t in props.get("TAM", {}).get("rich_text", [])
        )
        proxy_text = f"{key_insight}\n{tam}"

        print(f"  · {idea_name}")
        try:
            qc = run_pe3_qc(proxy_text, idea_name=idea_name, strict=False)
            notion_update_status(page_id, "✅ 완료",
                                 pe3_score=round(qc["overall"], 1) if qc["overall"] else None,
                                 pe3_grade=qc["grade"],
                                 pe3_failed_must=qc["failed_must"])
            if strict and qc["overall"] and qc["overall"] < 88:
                print(f"    ⚠️  {idea_name}: {qc['overall']:.1f}% < 88%")
                fail_count += 1
        except Exception as e:
            print(f"    ❌ 오류: {e}")
            fail_count += 1
    print(f"\n✅ revalidate-all 완료 | 실패: {fail_count}건")
    return 1 if fail_count else 0


# ── --pe3-dashboard 모드 ──────────────────────────────────────────────────────

def pe3_dashboard_mode() -> int:
    """
    Notion DB의 PE-3 점수 분포를 콘솔 대시보드로 출력.
    """
    print("\n📊 [PE-3 Dashboard] Notion DB 점수 현황")
    records = notion_query_all_completed()
    scores = []
    for rec in records:
        props = rec["properties"]
        score = props.get("PE3 Score", {}).get("number")
        idea  = "".join(
            t["plain_text"] for t in props.get("Idea Name", {}).get("title", [])
        ) or rec["id"][:8]
        scores.append((idea, score))

    scores.sort(key=lambda x: (x[1] or 0), reverse=True)
    sep = "─" * 60
    print(f"  {sep}")
    print(f"  {'아이디어명':<30} {'PE-3':>6}  그래프")
    print(f"  {sep}")
    for idea, sc in scores:
        if sc is None:
            bar, label = "░" * 20, "  N/A"
        else:
            filled = int(sc / 5)
            bar    = "█" * filled + "░" * (20 - filled)
            label  = f" {sc:5.1f}"
        print(f"  {idea[:30]:<30} {label}  [{bar}]")
    print(f"  {sep}")
    valid = [s for _, s in scores if s is not None]
    if valid:
        avg = sum(valid) / len(valid)
        print(f"  평균: {avg:.1f}  최고: {max(valid):.1f}  최저: {min(valid):.1f}  건수: {len(valid)}")
    print(f"  {sep}\n")
    return 0


# ── --ab-test 모드 ────────────────────────────────────────────────────────────

def ab_test_mode(v1_path: str, v2_path: str, strict: bool = False) -> int:
    """
    동일 아이디어에 v1 vs v2 프롬프트를 각각 적용해
    PE-3 QC 점수를 비교 출력 (API 미호출, 로컬 파일 기준).
    """
    if not _QC_AVAILABLE:
        print("❌ pe3_product_validator 모듈 없음")
        return 1

    print(f"\n🔬 [A/B Test] {Path(v1_path).name} vs {Path(v2_path).name}")
    results = {}
    for label, path in [("v1", v1_path), ("v2", v2_path)]:
        content = Path(path).read_text(encoding="utf-8")
        qc = run_pe3_qc(content, idea_name=label, strict=False)
        results[label] = qc
        print(f"  {label}: {qc['overall']:.1f}%  {qc['grade']}")

    sep = "─" * 56
    print(f"\n  {sep}")
    print(f"  {'항목':<20} {'v1':>8} {'v2':>8} {'Δ':>8}")
    print(f"  {sep}")
    for d_id in sorted(
        set(results["v1"]["raw"].get("dimensions", {}).keys()) |
        set(results["v2"]["raw"].get("dimensions", {}).keys())
    ):
        pct_v1 = results["v1"]["raw"].get("dimensions", {}).get(d_id, {}).get("pct", 0)
        pct_v2 = results["v2"]["raw"].get("dimensions", {}).get(d_id, {}).get("pct", 0)
        delta  = pct_v2 - pct_v1
        arrow  = "↑" if delta > 0 else ("↓" if delta < 0 else "─")
        print(f"  {d_id:<20} {pct_v1:>7.1f}% {pct_v2:>7.1f}% {arrow}{abs(delta):>6.1f}%")
    print(f"  {sep}")
    ov1 = results["v1"]["overall"]
    ov2 = results["v2"]["overall"]
    print(f"  Overall             {ov1:>7.1f}% {ov2:>7.1f}% {'↑' if ov2>ov1 else '↓'}{abs(ov2-ov1):>6.1f}%")
    print(f"  {sep}")
    winner = "v2" if ov2 >= ov1 else "v1"
    print(f"  🏆 권장 채택: {winner} ({results[winner]['grade']})")
    print(f"  {sep}\n")
    return 0


# ── 메인 폴링 루프 ────────────────────────────────────────────────────────────

def run_once(dry_run: bool = False, record_id: str = None,
             qc_strict: bool = False) -> list:
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
        description="PE-7 Product Idea → MECE 자동분석 루프 v2.0"
    )
    parser.add_argument("--watch",          action="store_true", help="반복 폴링 모드")
    parser.add_argument("--dry-run",        action="store_true", help="API 미호출")
    parser.add_argument("--qc-only",        action="store_true", help="로컬 파일 QC")
    parser.add_argument("--file",           help="--qc-only / --ab-test v1 대상")
    parser.add_argument("--qc-strict",      action="store_true", help="88점 미만 중단")
    parser.add_argument("--record-id",      help="특정 Notion 페이지 ID")
    parser.add_argument("--output",         help="결과 JSON 저장")
    parser.add_argument("--revalidate-all", action="store_true",
                        help="Notion 완료 레코드 전체 QC 재검증")
    parser.add_argument("--pe3-dashboard",  action="store_true",
                        help="PE-3 점수 대시보드 출력")
    parser.add_argument("--ab-test",        action="store_true",
                        help="v1 vs v2 A/B 비교 (--v1 --v2 필요)")
    parser.add_argument("--v1",             help="A/B 테스트 v1 파일 경로")
    parser.add_argument("--v2",             help="A/B 테스트 v2 파일 경로")
    parser.add_argument("--prompt-version", default="v2",
                        help="프롬프트 버전 태그 (기본: v2)")
    args = parser.parse_args()

    # ── 특수 모드들 ──
    if args.qc_only:
        if not args.file:
            print("❌ --qc-only 모드에는 --file 경로 필요")
            sys.exit(1)
        sys.exit(qc_only_mode(args.file, strict=args.qc_strict))

    if args.revalidate_all:
        sys.exit(revalidate_all_mode(strict=args.qc_strict))

    if args.pe3_dashboard:
        sys.exit(pe3_dashboard_mode())

    if args.ab_test:
        if not (args.v1 and args.v2):
            print("❌ --ab-test 모드에는 --v1 --v2 파일 경로 필요")
            sys.exit(1)
        sys.exit(ab_test_mode(args.v1, args.v2, strict=args.qc_strict))

    if not NOTION_TOKEN and not args.dry_run:
        print("❌ NOTION_TOKEN 미설정"); sys.exit(1)
    if not OPENAI_KEY and not args.dry_run:
        print("❌ OPENAI_API_KEY 미설정"); sys.exit(1)

    qc_status = "✅ 활성" if _QC_AVAILABLE else "⚠️ 미임포트"
    print("🚀 PE-7 Product Idea → MECE 자동분석 루프 v2.0")
    print(f"   DB ID          : {DB_ID}")
    print(f"   Dry-Run        : {args.dry_run}")
    print(f"   Watch          : {args.watch}")
    print(f"   PE-3 QC        : {qc_status}")
    print(f"   QC Strict      : {args.qc_strict}")
    print(f"   Prompt Version : {args.prompt_version}")

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
