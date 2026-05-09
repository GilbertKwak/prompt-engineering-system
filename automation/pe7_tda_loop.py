#!/usr/bin/env python3
"""
pe7_tda_loop.py  v1.0
PE-TDA 자동화 실행 루프 — 6-STEP 파이프라인

역할:
  - PE-TDA 전체 워크플로우를 단일 진입점으로 연결
  - scripts/pe3_tda_validator.py v2.0 사용
  - Notion PE-TDA Master DB v2.0 연동
  - 6개 실행 모드: single | batch | qc-only | revalidate-all | pe3-dashboard | cross-fin

사용법:
  # STEP 1: 단일 실행 (반도체 DD)
  python automation/pe7_tda_loop.py \\
    --tech "HBM4" --company "SK하이닉스" \\
    --industry Semiconductor \\
    --mode Investment --depth DueDiligence \\
    --output Due_Diligence_Report \\
    --investment-size 5000 --target-irr 25 \\
    --qc-strict

  # STEP 2: AI/LLM 전략 분석
  python automation/pe7_tda_loop.py \\
    --tech "LLM Inference Engine" \\
    --industry AI --mode TechStrategy \\
    --depth Strategic --output Board_Presentation \\
    --qc-strict

  # STEP 3: 빠른 Summary
  python automation/pe7_tda_loop.py \\
    --tech "[기술명]" --industry AUTO --mode AUTO \\
    --depth Summary --output Executive_Report

  # STEP 4: 전체 PE-TDA Notion 레코드 재검증
  python automation/pe7_tda_loop.py --revalidate-all --qc-strict

  # STEP 5: PE-FIN IRR 연동 분석
  python automation/pe7_tda_loop.py \\
    --tech "[기술명]" --cross-fin \\
    --entry-ev 1000 --target-irr 25 \\
    --irr-bear 18.5 --irr-base 26.2

  # STEP 6: PE-3 대시보드
  python automation/pe7_tda_loop.py --pe3-dashboard
"""

import argparse
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional

try:
    from notion_client import Client as NotionClient
except ImportError:
    NotionClient = None

# ── 경로 설정 ───────────────────────────────────────

ROOT       = Path(__file__).resolve().parent.parent
VALIDATOR  = ROOT / "scripts" / "pe3_tda_validator.py"   # v2.0 사용
PROMPT_DIR = ROOT / "prompts" / "PE-TDA"
LOG_DIR    = ROOT / "logs" / "pe7_tda"
SESSION_LOG = LOG_DIR / f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

# Notion PE-TDA Master DB v2.0 (collection://546c6ac2-...)
NOTION_DB_ID = os.environ.get(
    "PE_TDA_DB_ID",
    "83fae865ceb146f6b873e136d503566d"
)

VERSION = "1.0"

# 산업별 기본 데프스 맵
INDUSTRY_DEPTH_DEFAULTS = {
    "Semiconductor": "DueDiligence",
    "Bio":           "DueDiligence",
    "AI":            "Strategic",
    "FinTech":       "Strategic",
    "Energy":        "Strategic",
    "Defense":       "DueDiligence",
    "Manufacturing": "Strategic",
    "Mobility":      "Strategic",
}

# 프롬프트 매핑 (industry → 파일명)
PROMPT_FILE_MAP = {
    "AI":            "pe_tda_orch_v2.0.md",
    "Semiconductor": "pe_tda_orch_v2.0.md",
    "Bio":           "pe_tda_orch_v2.0.md",
    "Manufacturing": "pe_tda_orch_v2.0.md",
    "Energy":        "pe_tda_orch_v2.0.md",
    "Defense":       "pe_tda_orch_v2.0.md",
    "FinTech":       "pe_tda_orch_v2.0.md",
    "Mobility":      "pe_tda_orch_v2.0.md",
    "AUTO":          "pe_tda_orch_v2.0.md",
}


# ============================================================
# 1. 데이터 구조
# ============================================================

@dataclass
class TDAJob:
    """PE-TDA 실행 작업 단위"""
    tech:          str   = ""
    company:       str   = ""
    industry:      str   = "AI"
    mode:          str   = "Investment"
    depth:         str   = "Strategic"
    output:        str   = "Executive_Report"
    investment_size: float = 0.0
    target_irr:    float = 20.0
    geo:           str   = "KR"
    base_year:     int   = 2026
    # D1~D5 점수 (live 모드)
    d1: float = 0.0
    d2: float = 0.0
    d3: float = 0.0
    d4: float = 0.0
    d5: float = 0.0
    industry_score: float = 0.0
    # MECE 체크
    mece_no_overlap:    bool = False
    mece_no_gap:        bool = False
    mece_logic_layer:   bool = False
    mece_industry_add:  bool = False
    mece_auto_detect:   bool = False
    # PE-FIN IRR
    irr_base:     float = 0.0
    irr_bear:     float = 0.0
    entry_ev:     float = 0.0
    irr_ev_cap:   float = 0.0
    irr_bear_gate: bool = False
    irr_sensitivity: bool = False
    # 리스크 & 운영
    risk_level:    str = "Yellow"
    key_insight:   str = ""
    deliverable_url: str = ""
    # Notion
    page_id: str = ""
    dry_run: bool = False


@dataclass
class TDAJobResult:
    """pe3_tda_validator.py 실행 결과"""
    job:          TDAJob = field(default_factory=TDAJob)
    returncode:   int    = -1
    stdout:       str    = ""
    stderr:       str    = ""
    score:        float  = 0.0
    grade:        str    = "?"
    risk_level:   str    = "?"
    irr_bear_gate: str   = "?"
    failed_musts: list   = field(default_factory=list)
    elapsed_sec:  float  = 0.0
    timestamp:    str    = field(default_factory=lambda: datetime.now().isoformat())

    @property
    def passed(self) -> bool:
        return self.returncode == 0


# ============================================================
# 2. 세션 로겅
# ============================================================

class SessionLogger:
    def __init__(self, log_path: Path):
        self.log_path = log_path
        self.records: List[dict] = []
        log_path.parent.mkdir(parents=True, exist_ok=True)

    def add(self, result: TDAJobResult) -> None:
        self.records.append({
            "timestamp":    result.timestamp,
            "tech":         result.job.tech,
            "company":      result.job.company,
            "industry":     result.job.industry,
            "score":        result.score,
            "grade":        result.grade,
            "risk_level":   result.risk_level,
            "irr_bear_gate":result.irr_bear_gate,
            "failed_musts": result.failed_musts,
            "elapsed_sec":  result.elapsed_sec,
            "returncode":   result.returncode,
        })

    def save(self) -> None:
        with open(self.log_path, "w", encoding="utf-8") as f:
            json.dump(self.records, f, ensure_ascii=False, indent=2)
        print(f"\n[LOG] 세션 로그 저장: {self.log_path}")


# ============================================================
# 3. 유효성 검사
# ============================================================

def _check_validator() -> None:
    if not VALIDATOR.exists():
        print(f"[ERROR] Validator 미확인: {VALIDATOR}")
        print("  실행: scripts/pe3_tda_validator.py v2.0 이상 필요")
        sys.exit(1)


def _resolve_industry(industry: str) -> str:
    """실행 전 AUTO 산업 자동 탐지 (테크명 키워드 기반)"""
    if industry.upper() != "AUTO":
        return industry
    return "AI"  # 기본값; 실제 Auto-Detection은 LLM 표준 입력에서 수행


def _resolve_depth(industry: str, depth: str) -> str:
    if depth.upper() == "AUTO":
        return INDUSTRY_DEPTH_DEFAULTS.get(industry, "Strategic")
    return depth


# ============================================================
# 4. 실행 코어: subprocess 라운더
# ============================================================

def _build_validator_cmd(job: TDAJob, qc_strict: bool = False) -> list:
    """
pe3_tda_validator.py --live 모드 명령어 조립
    """
    cmd = [
        sys.executable, str(VALIDATOR),
        "--live",
        "--industry",       job.industry,
        "--mode",           job.mode,
        "--depth",          job.depth,
        "--tech-name",      job.tech,
        "--company",        job.company,
        "--d1-score",       str(job.d1),
        "--d2-score",       str(job.d2),
        "--d3-score",       str(job.d3),
        "--d4-score",       str(job.d4),
        "--d5-score",       str(job.d5),
        "--industry-score", str(job.industry_score),
        "--irr-base",       str(job.irr_base),
        "--irr-bear",       str(job.irr_bear),
        "--entry-ev",       str(job.entry_ev),
        "--irr-ev-cap",     str(job.irr_ev_cap),
        "--target-irr",     str(job.target_irr),
        "--risk-level",     job.risk_level,
        "--key-insight",    job.key_insight,
        "--target-score",   "95",
    ]
    # MECE 플래그
    if job.mece_no_overlap:    cmd.append("--mece-no-overlap")
    if job.mece_no_gap:        cmd.append("--mece-no-gap")
    if job.mece_logic_layer:   cmd.append("--mece-logic-layer")
    if job.mece_industry_add:  cmd.append("--mece-industry-add")
    if job.mece_auto_detect:   cmd.append("--mece-auto-detect")
    # IRR 플래그
    if job.irr_bear_gate:      cmd.append("--irr-bear-gate")
    if job.irr_sensitivity:    cmd.append("--irr-sensitivity")
    # Notion
    if job.page_id:
        cmd.extend(["--page-id", job.page_id])
    if job.dry_run:
        cmd.append("--dry-run")
    if job.deliverable_url:
        cmd.extend(["--deliverable-url", job.deliverable_url])
    # QC
    if qc_strict:
        cmd.append("--qc-strict")
    return cmd


def _run_job(job: TDAJob, qc_strict: bool = False) -> TDAJobResult:
    """
    단일 TDAJob 실행 → TDAJobResult 반환
    """
    result = TDAJobResult(job=job)
    cmd = _build_validator_cmd(job, qc_strict=qc_strict)

    print(f"\n{'='*60}")
    print(f"  [PE-TDA] 실행: {job.tech or '(static)'} | {job.industry} | {job.mode}/{job.depth}")
    print(f"  명령어: {' '.join(cmd[:6])} ...")
    print(f"{'='*60}")

    t0 = time.monotonic()
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    result.elapsed_sec = round(time.monotonic() - t0, 2)
    result.returncode  = proc.returncode
    result.stdout      = proc.stdout
    result.stderr      = proc.stderr

    # stdout 파싱
    for line in proc.stdout.splitlines():
        if "제: " in line and "|점수" in line:
            # "평점: {score}/100" 패턴
            parts = line.split("|")
            for p in parts:
                if "점수:" in p:
                    try:
                        result.score = float(p.split(":")[1].strip().split("/")[0])
                    except Exception:
                        pass
                if "등급" in p or "Grade" in p:
                    for g in ["A+", "A", "B+", "B", "C", "D"]:
                        if g in p:
                            result.grade = g
                            break
        if "MUST 미통과" in line and "→" in line:
            raw = line.split("→")[-1].strip()
            result.failed_musts = [x.strip() for x in raw.split(",") if x.strip()]
        if "Bear Gate:" in line:
            result.irr_bear_gate = line.split(":")[-1].strip()
        if "리스크:" in line:
            for risk in ["Green", "Yellow", "Red"]:
                if risk in line:
                    result.risk_level = risk
                    break

    print(proc.stdout)
    if proc.stderr:
        print(f"[STDERR] {proc.stderr[:500]}", file=sys.stderr)

    return result


# ============================================================
# 5. 정적 분석 모드 (--qc-only)
# ============================================================

def run_qc_only(
    file_path: str,
    target_score: float = 95.0,
    qc_strict: bool = False
) -> TDAJobResult:
    """
    프롬프트 .md 파일 정적 QC 검증
    """
    result = TDAJobResult()
    cmd = [
        sys.executable, str(VALIDATOR),
        "--file", file_path,
        "--target-score", str(target_score),
    ]
    if qc_strict:
        cmd.append("--qc-strict")

    print(f"\n[QC-ONLY] 정적 분석: {file_path}")
    t0 = time.monotonic()
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    result.elapsed_sec  = round(time.monotonic() - t0, 2)
    result.returncode   = proc.returncode
    result.stdout       = proc.stdout
    result.stderr       = proc.stderr
    print(proc.stdout)
    return result


# ============================================================
# 6. Notion 배치 재검증 (--revalidate-all)
# ============================================================

def run_revalidate_all(
    qc_strict: bool = False,
    dry_run:   bool = False,
    target_score: float = 95.0,
) -> List[TDAJobResult]:
    """
    Notion PE-TDA Master DB v2.0의 모든 레코드를 가져와
    점수 < target_score 인 항목만 재검증
    """
    if NotionClient is None:
        print("[ERROR] notion-client 미설치: pip install notion-client")
        sys.exit(1)

    token = os.environ.get("NOTION_TOKEN")
    if not token:
        print("[ERROR] 환경변수 NOTION_TOKEN 미설정")
        sys.exit(1)

    notion  = NotionClient(auth=token)
    results = []

    print(f"\n[REVALIDATE-ALL] PE-TDA Master DB 이터레이팅...")
    print(f"  DB ID   : {NOTION_DB_ID}")
    print(f"  목표점수: {target_score}+   QC-strict: {qc_strict}")

    # Notion DB 페이지 조회
    has_more    = True
    start_cursor = None
    all_pages   = []

    while has_more:
        kwargs = {"database_id": NOTION_DB_ID, "page_size": 20}
        if start_cursor:
            kwargs["start_cursor"] = start_cursor
        resp = notion.databases.query(**kwargs)
        all_pages.extend(resp.get("results", []))
        has_more     = resp.get("has_more", False)
        start_cursor = resp.get("next_cursor")

    print(f"  총 {len(all_pages)}개 레코드 조회")

    revalidate_targets = []
    for page in all_pages:
        props = page.get("properties", {})
        # PE3 Score 추출
        score_prop = props.get("PE3 Score", {})
        current_score = score_prop.get("number") or 0.0
        grade_prop = props.get("PE3 Grade", {})
        current_grade = ""
        if grade_prop.get("select"):
            current_grade = grade_prop["select"].get("name", "")

        if current_score < target_score:
            page_id   = page["id"]
            tech_name = ""
            title_prop = props.get("Tech Name", {})
            if title_prop.get("title"):
                tech_name = title_prop["title"][0]["plain_text"]

            industry = ""
            ind_prop = props.get("D6 Industry Layer", {})
            if ind_prop.get("select"):
                industry = ind_prop["select"].get("name", "AI")

            revalidate_targets.append({
                "page_id":       page_id,
                "tech":          tech_name,
                "industry":      industry or "AI",
                "current_score": current_score,
                "current_grade": current_grade,
            })

    print(f"  재검증 대상: {len(revalidate_targets)}개 (점수 {target_score}미만)")

    for target in revalidate_targets:
        print(f"\n  ▶ [{target['tech']}] 현재: {target['current_score']}점 ({target['current_grade']}) → 재검증")
        job = TDAJob(
            tech=target["tech"],
            industry=target["industry"],
            page_id=target["page_id"],
            dry_run=dry_run,
        )
        r = _run_job(job, qc_strict=qc_strict)
        results.append(r)

        status = "✅ 통과" if r.passed else "❌ 실패"
        print(f"  {status} | 점수: {r.score} | 등급: {r.grade} | {r.elapsed_sec}s")

    return results


# ============================================================
# 7. PE-3 대시보드 (--pe3-dashboard)
# ============================================================

def run_pe3_dashboard() -> None:
    """
    Notion PE-TDA Master DB v2.0를 고성능 클러스터로
    요약해서 출력
    """
    if NotionClient is None:
        print("[ERROR] notion-client 미설치: pip install notion-client")
        sys.exit(1)

    token = os.environ.get("NOTION_TOKEN")
    if not token:
        print("[ERROR] 환경변수 NOTION_TOKEN 미설정")
        sys.exit(1)

    notion = NotionClient(auth=token)

    has_more = True
    start_cursor = None
    pages = []
    while has_more:
        kwargs = {"database_id": NOTION_DB_ID, "page_size": 50}
        if start_cursor:
            kwargs["start_cursor"] = start_cursor
        resp = notion.databases.query(**kwargs)
        pages.extend(resp.get("results", []))
        has_more     = resp.get("has_more", False)
        start_cursor = resp.get("next_cursor")

    total     = len(pages)
    grade_cnt = {"A+": 0, "A": 0, "B+": 0, "B": 0, "C": 0, "D": 0}
    risk_cnt  = {"Green": 0, "Yellow": 0, "Red": 0}
    ind_cnt   = {}
    scores    = []

    for page in pages:
        props = page.get("properties", {})

        # 등급
        gp = props.get("PE3 Grade", {}).get("select") or {}
        g  = gp.get("name", "")
        if g in grade_cnt:
            grade_cnt[g] += 1

        # 리스크
        rp = props.get("TDA Risk Level", {}).get("select") or {}
        r  = rp.get("name", "")
        if r in risk_cnt:
            risk_cnt[r] += 1

        # 산업
        ip = props.get("D6 Industry Layer", {}).get("select") or {}
        ind = ip.get("name", "Unknown")
        ind_cnt[ind] = ind_cnt.get(ind, 0) + 1

        # 점수
        sp = props.get("PE3 Score", {}).get("number")
        if sp is not None:
            scores.append(sp)

    avg_score  = round(sum(scores) / len(scores), 1) if scores else 0.0
    above_95   = sum(1 for s in scores if s >= 95)
    above_88   = sum(1 for s in scores if s >= 88)

    print("\n" + "═" * 65)
    print("  PE-TDA Master DB v2.0 | PE-3 대시보드")
    print("═" * 65)
    print(f"  총 레코드    : {total}")
    print(f"  평균 점수   : {avg_score}")
    print(f"  A+ (95+)  : {above_95}개 ({round(above_95/total*100,1) if total else 0}%)")
    print(f"  A  (88+)  : {above_88}개 ({round(above_88/total*100,1) if total else 0}%)")

    print("\n  [등급 분포]")
    for g, cnt in sorted(grade_cnt.items()):
        bar = "█" * cnt
        print(f"    {g:3s} : {cnt:3d}  {bar}")

    print("\n  [리스크 분포]")
    r_emoji = {"Green": "🟢", "Yellow": "🟡", "Red": "🔴"}
    for rv, cnt in sorted(risk_cnt.items()):
        print(f"    {r_emoji.get(rv,'')} {rv:8s}: {cnt:3d}")

    print("\n  [산업별 레코드]")
    for ind, cnt in sorted(ind_cnt.items(), key=lambda x: -x[1]):
        print(f"    {ind:15s}: {cnt:3d}")

    print("\n" + "═" * 65)


# ============================================================
# 8. PE-FIN 연동 모드 (--cross-fin)
# ============================================================

def run_cross_fin(args, qc_strict: bool = False) -> TDAJobResult:
    """
    PE-FIN IRR 연동 모드
    FIN-06-BFA IRR 역산 결과를 PE-TDA D6 Bear Gate에 직접 주입
    """
    print("\n[CROSS-FIN] PE-FIN IRR → PE-TDA D6 Bear Gate 연동")
    print(f"  Entry EV   : {args.entry_ev} M")
    print(f"  IRR Bear   : {args.irr_bear}%")
    print(f"  IRR Base   : {args.irr_base}%")
    print(f"  Target IRR : {args.target_irr}%")

    bear_gate_pass = args.irr_bear >= args.target_irr * 0.75
    print(f"  Bear Gate  : {'PASS ✅' if bear_gate_pass else 'FAIL ❌'} "
          f"({args.irr_bear:.1f}% {'\u2265' if bear_gate_pass else '<'} "
          f"{args.target_irr * 0.75:.1f}%)")

    job = TDAJob(
        tech=args.tech or "PE-FIN연동분석",
        company=args.company or "",
        industry=_resolve_industry(args.industry),
        mode=args.mode,
        depth=_resolve_depth(_resolve_industry(args.industry), args.depth),
        irr_base=args.irr_base,
        irr_bear=args.irr_bear,
        entry_ev=args.entry_ev,
        irr_ev_cap=args.irr_ev_cap,
        target_irr=args.target_irr,
        irr_bear_gate=bear_gate_pass,
        irr_sensitivity=getattr(args, 'irr_sensitivity', False),
        d1=getattr(args, 'd1', 0.0),
        d2=getattr(args, 'd2', 0.0),
        d3=getattr(args, 'd3', 0.0),
        d4=getattr(args, 'd4', 0.0),
        d5=getattr(args, 'd5', 0.0),
        industry_score=getattr(args, 'industry_score', 0.0),
        risk_level=args.risk_level,
        key_insight=getattr(args, 'key_insight', ""),
        page_id=args.page_id,
        dry_run=args.dry_run,
    )
    return _run_job(job, qc_strict=qc_strict)


# ============================================================
# 9. 배치 모드 (--batch)
# ============================================================

def run_batch(
    batch_file: str,
    qc_strict:  bool = False,
    dry_run:    bool = False,
) -> List[TDAJobResult]:
    """
    JSON 배치 파일로 PE-TDA 다수 효속 실행

    JSON 형식:
    [
      {"tech": "HBM4", "company": "SKH", "industry": "Semiconductor",
       "d1": 15, "d2": 14, "d3": 13, "d4": 13, "d5": 14,
       "industry_score": 17, "irr_bear": 19.8, "target_irr": 25, ...},
      ...
    ]
    """
    with open(batch_file, "r", encoding="utf-8") as f:
        jobs_raw = json.load(f)

    results = []
    total   = len(jobs_raw)
    print(f"\n[BATCH] {total}개 작업 시작")

    for i, raw in enumerate(jobs_raw, 1):
        industry = _resolve_industry(raw.get("industry", "AI"))
        depth    = _resolve_depth(industry, raw.get("depth", "AUTO"))

        job = TDAJob(
            tech=raw.get("tech", ""),
            company=raw.get("company", ""),
            industry=industry,
            mode=raw.get("mode", "Investment"),
            depth=depth,
            output=raw.get("output", "Executive_Report"),
            investment_size=float(raw.get("investment_size", 0)),
            target_irr=float(raw.get("target_irr", 20)),
            d1=float(raw.get("d1", 0)),
            d2=float(raw.get("d2", 0)),
            d3=float(raw.get("d3", 0)),
            d4=float(raw.get("d4", 0)),
            d5=float(raw.get("d5", 0)),
            industry_score=float(raw.get("industry_score", 0)),
            mece_no_overlap=bool(raw.get("mece_no_overlap", False)),
            mece_no_gap=bool(raw.get("mece_no_gap", False)),
            mece_logic_layer=bool(raw.get("mece_logic_layer", False)),
            mece_industry_add=bool(raw.get("mece_industry_add", False)),
            mece_auto_detect=bool(raw.get("mece_auto_detect", False)),
            irr_base=float(raw.get("irr_base", 0)),
            irr_bear=float(raw.get("irr_bear", 0)),
            entry_ev=float(raw.get("entry_ev", 0)),
            irr_ev_cap=float(raw.get("irr_ev_cap", 0)),
            irr_bear_gate=bool(raw.get("irr_bear_gate", False)),
            irr_sensitivity=bool(raw.get("irr_sensitivity", False)),
            risk_level=raw.get("risk_level", "Yellow"),
            key_insight=raw.get("key_insight", ""),
            deliverable_url=raw.get("deliverable_url", ""),
            page_id=raw.get("page_id", ""),
            dry_run=dry_run,
        )

        print(f"\n[{i}/{total}] {job.tech} | {job.industry}")
        r = _run_job(job, qc_strict=qc_strict)
        results.append(r)

    return results


# ============================================================
# 10. 요약 리포트
# ============================================================

def _print_summary(results: List[TDAJobResult]) -> None:
    if not results:
        return

    passed = [r for r in results if r.passed]
    failed = [r for r in results if not r.passed]
    avg    = round(sum(r.score for r in results) / len(results), 1)

    print("\n" + "═" * 65)
    print(f"  PE-7 TDA Loop 요약  |  이 시간: {datetime.now().strftime('%H:%M:%S')}")
    print("═" * 65)
    print(f"  총 작업: {len(results)}   ✅ 통과: {len(passed)}   ❌ 실패: {len(failed)}")
    print(f"  평균 PE3 점수: {avg}")

    if failed:
        print("\n  [통과 실패 항목]")
        for r in failed:
            print(f"    ❌ {r.job.tech or '(static)'} | 점수: {r.score} | MUST: {', '.join(r.failed_musts) or '없음'}")

    if passed:
        print("\n  [통과 항목]")
        for r in passed:
            print(f"    ✅ {r.job.tech or '(static)'} | {r.grade} | {r.score}점")

    print("═" * 65)


# ============================================================
# 11. CLI 진입점
# ============================================================

def parse_args():
    p = argparse.ArgumentParser(
        description="PE-TDA 자동화 실행 루프 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # 실행 모드
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--single",         action="store_true",  help="단일 분석 (기본 모드)")
    mode.add_argument("--batch",          metavar="JSON_FILE",  help="JSON 배치 파일")
    mode.add_argument("--qc-only",        metavar="MD_FILE",    help="프롬프트 정적 QC만")
    mode.add_argument("--revalidate-all", action="store_true",  help="Notion DB 전체 재검증")
    mode.add_argument("--pe3-dashboard",  action="store_true",  help="PE-3 대시보드")
    mode.add_argument("--cross-fin",      action="store_true",  help="PE-FIN IRR 연동 실행")

    # 단일/배치 공통
    p.add_argument("--tech",             type=str,   default="")
    p.add_argument("--company",          type=str,   default="")
    p.add_argument("--industry",         type=str,   default="AUTO")
    p.add_argument("--mode",             type=str,   default="Investment")
    p.add_argument("--depth",            type=str,   default="AUTO")
    p.add_argument("--output",           type=str,   default="Executive_Report")
    p.add_argument("--investment-size",  type=float, default=0.0)
    p.add_argument("--target-irr",       type=float, default=20.0)
    p.add_argument("--geo",              type=str,   default="KR")

    # D1~D5
    p.add_argument("--d1",               type=float, default=0.0)
    p.add_argument("--d2",               type=float, default=0.0)
    p.add_argument("--d3",               type=float, default=0.0)
    p.add_argument("--d4",               type=float, default=0.0)
    p.add_argument("--d5",               type=float, default=0.0)
    p.add_argument("--industry-score",   type=float, default=0.0)

    # MECE
    p.add_argument("--mece-no-overlap",  action="store_true")
    p.add_argument("--mece-no-gap",      action="store_true")
    p.add_argument("--mece-logic-layer", action="store_true")
    p.add_argument("--mece-industry-add",action="store_true")
    p.add_argument("--mece-auto-detect", action="store_true")

    # PE-FIN IRR
    p.add_argument("--irr-base",         type=float, default=0.0)
    p.add_argument("--irr-bear",         type=float, default=0.0)
    p.add_argument("--entry-ev",         type=float, default=0.0)
    p.add_argument("--irr-ev-cap",       type=float, default=0.0)
    p.add_argument("--irr-bear-gate",    action="store_true")
    p.add_argument("--irr-sensitivity",  action="store_true")

    # 리스크 & 운영
    p.add_argument("--risk-level",       type=str,   default="Yellow")
    p.add_argument("--key-insight",      type=str,   default="")
    p.add_argument("--deliverable-url",  type=str,   default="")

    # Notion & QC
    p.add_argument("--page-id",          type=str,   default="")
    p.add_argument("--dry-run",          action="store_true")
    p.add_argument("--qc-strict",        action="store_true")
    p.add_argument("--target-score",     type=float, default=95.0)
    p.add_argument("--no-log",           action="store_true", help="세션 로그 누락")

    return p.parse_args()


def main():
    args   = parse_args()
    logger = SessionLogger(SESSION_LOG)
    _check_validator()

    results: List[TDAJobResult] = []

    # ── 모드 분기 ─────────────────────────────

    if args.qc_only:
        r = run_qc_only(args.qc_only, args.target_score, args.qc_strict)
        results.append(r)

    elif args.revalidate_all:
        results = run_revalidate_all(
            qc_strict=args.qc_strict,
            dry_run=args.dry_run,
            target_score=args.target_score,
        )

    elif args.pe3_dashboard:
        run_pe3_dashboard()
        return  # 로그 불필요

    elif args.cross_fin:
        r = run_cross_fin(args, qc_strict=args.qc_strict)
        results.append(r)

    elif args.batch:
        results = run_batch(
            args.batch,
            qc_strict=args.qc_strict,
            dry_run=args.dry_run,
        )

    else:
        # 단일 모드 (기본값)
        industry = _resolve_industry(args.industry)
        depth    = _resolve_depth(industry, args.depth)

        job = TDAJob(
            tech=args.tech,
            company=args.company,
            industry=industry,
            mode=args.mode,
            depth=depth,
            output=args.output,
            investment_size=args.investment_size,
            target_irr=args.target_irr,
            geo=args.geo,
            d1=args.d1,
            d2=args.d2,
            d3=args.d3,
            d4=args.d4,
            d5=args.d5,
            industry_score=args.industry_score,
            mece_no_overlap=args.mece_no_overlap,
            mece_no_gap=args.mece_no_gap,
            mece_logic_layer=args.mece_logic_layer,
            mece_industry_add=args.mece_industry_add,
            mece_auto_detect=args.mece_auto_detect,
            irr_base=args.irr_base,
            irr_bear=args.irr_bear,
            entry_ev=args.entry_ev,
            irr_ev_cap=args.irr_ev_cap,
            irr_bear_gate=args.irr_bear_gate,
            irr_sensitivity=args.irr_sensitivity,
            risk_level=args.risk_level,
            key_insight=args.key_insight,
            deliverable_url=args.deliverable_url,
            page_id=args.page_id,
            dry_run=args.dry_run,
        )
        r = _run_job(job, qc_strict=args.qc_strict)
        results.append(r)

    # ── 요약 & 로그 ──────────────────────────

    if results:
        _print_summary(results)
        if not args.no_log:
            for r in results:
                logger.add(r)
            logger.save()

    # ── CI exit code ──────────────────────────
    if args.qc_strict and results:
        any_failed = any(not r.passed for r in results)
        if any_failed:
            sys.exit(1)


if __name__ == "__main__":
    main()
