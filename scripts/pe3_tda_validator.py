#!/usr/bin/env python3
"""
pe3_tda_validator.py  v2.0
PE-TDA MECE Technical Analysis Agent — PE-3 자동채점 엔진

[v2.0 변경사항]
  - D1~D5 MECE 5차원 채점 (기존 D6/D7/D8 TDA → 완전 재설계)
  - D6 산업특화 레이어 독립 채점 (8개 산업 가중치 적용)
  - PE-FIN IRR Bear Gate 연동 (FIN-06-BFA 직결)
  - Notion 19필드 자동기록
  - PE3 95+ 목표 등급체계 (A+ 등급 신설)
  - --file 모드: 프롬프트 파일 정적 분석
  - --live 모드: 실측값 기반 동적 채점
  - --revalidate-all: PE-TDA 전체 레코드 배치 재검증
  - --pe3-dashboard: 전체 도메인 PE-3 현황 출력

사용법:
  # 프롬프트 구조 정적 검증
  python scripts/pe3_tda_validator.py \\
    --file prompts/PE-TDA/pe_tda_orch_v2.0.md \\
    --target-score 95 --qc-strict

  # 실측값 기반 동적 채점 (PE-FIN 연동)
  python scripts/pe3_tda_validator.py \\
    --live --page-id <NOTION_PAGE_ID> \\
    --industry Semiconductor \\
    --irr-bear 18.5 --entry-ev 1200 --target-irr 25 \\
    --d1-score 17 --d2-score 16 --d3-score 15 \\
    --d4-score 14 --d5-score 15 \\
    --industry-score 16 \\
    --dry-run
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

try:
    from notion_client import Client as NotionClient
except ImportError:
    NotionClient = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ============================================================
# 1. 상수 & 설정
# ============================================================

VERSION = "2.0"

# D1~D5 각 차원 최대 배점 (합계 80점)
DIM_MAX = {
    "D1_tech_structure":     16,  # 기술구조
    "D2_performance":        16,  # 성능·확장성
    "D3_competitive":        16,  # 경쟁 차별화
    "D4_operational":        16,  # 운영 실행
    "D5_future_readiness":   16,  # 미래 대응
}

# D6 산업특화 최대 배점 (20점) — 8개 산업별 핵심 체크
INDUSTRY_MAX = 20

# 총점 = 80 + 20 = 100점
TOTAL_MAX = 100

# 산업별 D6 필수 체크항목 (MUST 항목 ID 목록)
INDUSTRY_MUST = {
    "AI":            ["D6-AI-01", "D6-AI-02", "D6-AI-03"],  # Architecture/Inference/DataMoat
    "Semiconductor": ["D6-SEMI-01", "D6-SEMI-02", "D6-SEMI-03"],  # Node/Yield/CAPEX
    "Bio":           ["D6-BIO-01", "D6-BIO-02", "D6-BIO-03"],  # MOA/Clinical/Regulatory
    "Manufacturing": ["D6-MFG-01", "D6-MFG-02"],  # ProcessYield/Automation
    "Energy":        ["D6-NRG-01", "D6-NRG-02", "D6-NRG-03"],  # EnergyDensity/Thermal/Material
    "Defense":       ["D6-DEF-01", "D6-DEF-02"],  # MissionReliability/Sovereignty
    "FinTech":       ["D6-FIN-01", "D6-FIN-02", "D6-FIN-03"],  # CoreEngine/Regulatory/FraudDetect
    "Mobility":      ["D6-MOB-01", "D6-MOB-02", "D6-MOB-03"],  # ADAS/FuncSafety/SensorFusion
}

# 산업별 D6 배점 가중치 (기술 복잡도 반영)
INDUSTRY_WEIGHT = {
    "AI":            1.0,
    "Semiconductor": 1.1,  # 공정/수율 복잡도 가산
    "Bio":           1.1,  # 임상/규제 복잡도 가산
    "Manufacturing": 0.9,
    "Energy":        1.0,
    "Defense":       1.0,
    "FinTech":       0.95,
    "Mobility":      1.0,
}

# PE-3 등급체계 (v2.0: A+ 신설, 95+ = A+)
GRADE_TABLE = [
    (95, 0,  "A+"),  # 95점 이상 + MUST 전통과
    (88, 0,  "A"),   # 88~94점 + MUST 전통과
    (78, 1,  "B+"),  # 78~87점 + MUST 1개 허용
    (65, 1,  "B"),   # 65~77점 + MUST 1개 허용
    (50, 2,  "C"),   # 50~64점 + MUST 2개 허용
    (0,  99, "D"),   # 50점 미만 또는 MUST 3개+
]


# ============================================================
# 2. 데이터 구조
# ============================================================

@dataclass
class TDAv2Input:
    """PE-TDA v2.0 입력값 (MECE D1~D5 + D6 산업특화 + PE-FIN)"""

    # ─ 기본 메타 ─
    tech_name:     str   = ""
    company:       str   = ""
    industry:      str   = "AI"       # 8개 산업 중 하나
    analysis_mode: str   = "Investment"
    analysis_depth:str   = "Strategic"
    base_year:     int   = 2026
    geo:           str   = "KR"

    # ─ MECE D1~D5 차원 점수 (각 0~16) ─
    d1_score: float = 0.0  # 기술구조
    d2_score: float = 0.0  # 성능·확장성
    d3_score: float = 0.0  # 경쟁 차별화
    d4_score: float = 0.0  # 운영 실행
    d5_score: float = 0.0  # 미래 대응

    # ─ D6 산업특화 점수 (0~20, 가중치 보정 전) ─
    industry_raw_score: float = 0.0

    # ─ MECE 자동보완 체크 (D1~D5 내부 체크리스트) ─
    mece_no_overlap:    bool = False  # 중복 항목 없음
    mece_no_gap:        bool = False  # 누락 영역 없음
    mece_logic_layer:   bool = False  # 논리 계층 정합
    mece_industry_add:  bool = False  # 산업특화 항목 추가 완료
    mece_auto_detect:   bool = False  # Auto-Detection 실행됨

    # ─ PE-FIN IRR 연동 (FIN-06-BFA) ─
    irr_base:           float = 0.0
    irr_bear:           float = 0.0
    entry_ev:           float = 0.0   # USD M
    irr_entry_ev_cap:   float = 0.0   # USD M (IRR 역산 EV 상한)
    target_irr:         float = 20.0  # % 목표 IRR
    irr_bear_gate_pass: bool  = False  # Bear 시나리오 통과 여부
    irr_sensitivity_ok: bool  = False  # Exit ±1x 감응도 통과

    # ─ 운영 보조 필드 ─
    tda_risk_level:  str = "Yellow"  # Green | Yellow | Red
    key_insight:     str = ""
    deliverable_url: str = ""
    notion_page_id:  str = ""


@dataclass
class TDAv2Result:
    """PE-3 채점 결과 컨테이너"""
    total_score:       float = 0.0
    grade:             str   = "D"
    mece_dim_scores:   dict  = field(default_factory=dict)  # D1~D5 점수
    industry_score:    float = 0.0                           # D6 가중 점수
    failed_must_ids:   list  = field(default_factory=list)
    passed_must_ids:   list  = field(default_factory=list)
    mece_check_passed: bool  = False
    irr_bear_gate:     str   = "PENDING"
    tda_risk_level:    str   = "Yellow"
    warnings:          list  = field(default_factory=list)
    suggestions:       list  = field(default_factory=list)
    timestamp:         str   = field(default_factory=lambda: datetime.now().isoformat())


# ============================================================
# 3. 정적 분석 (--file 모드)
# ============================================================

class PromptStaticAnalyzer:
    """
    프롬프트 .md 파일을 읽어 구조 완전성 검증.
    실제 LLM 호출 없이 텍스트 패턴으로 MECE 점수 추정.
    """

    # 필수 섹션 존재 여부 패턴
    REQUIRED_SECTIONS = [
        (r"ROLE|역할",           "ROLE 정의",           4),
        (r"INPUT.*SCHEMA",       "INPUT 스키마",         4),
        (r"Auto.?Detection",     "Auto-Detection 엔진",  4),
        (r"D1.*Technology",      "D1 기술구조",          8),
        (r"D2.*Performance",     "D2 성능확장",          8),
        (r"D3.*Competitive",     "D3 경쟁차별화",        8),
        (r"D4.*Operational",     "D4 운영실행",          8),
        (r"D5.*Future",          "D5 미래대응",          8),
        (r"Industry.*Special",   "산업특화 레이어",      10),
        (r"MECE.*[Rr]isk",       "MECE 리스크맵",        6),
        (r"PE-3.*자가채점",       "PE-3 자가채점",        6),
        (r"PE-FIN|IRR|Entry.?EV","PE-FIN 연동 필드",     8),
        (r"Notion.*연동|NOTION", "Notion 연동 출력",     6),
        (r"CROSS.*PE-",          "Cross-Link 정의",      4),
        (r"[Ff]in[Tt]ech|금융기술","FinTech 산업 특화",  5),
        (r"[Mm]obilit|자동차",   "Mobility 산업 특화",   5),
    ]

    def analyze(self, filepath: str) -> TDAv2Result:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        result = TDAv2Result()
        total = 0.0
        failed_musts = []
        warnings = []
        suggestions = []

        # 섹션별 점수 산정
        dim_map = {"D1": 0, "D2": 0, "D3": 0, "D4": 0, "D5": 0}
        industry_pts = 0
        meta_pts = 0

        for pattern, label, pts in self.REQUIRED_SECTIONS:
            found = bool(re.search(pattern, text))
            if found:
                total += pts
                if label.startswith("D1"):
                    dim_map["D1"] += pts
                elif label.startswith("D2"):
                    dim_map["D2"] += pts
                elif label.startswith("D3"):
                    dim_map["D3"] += pts
                elif label.startswith("D4"):
                    dim_map["D4"] += pts
                elif label.startswith("D5"):
                    dim_map["D5"] += pts
                elif "산업특화" in label or "FinTech" in label or "Mobility" in label:
                    industry_pts += pts
                else:
                    meta_pts += pts
            else:
                is_must = pts >= 8
                item_id = f"STATIC-{label[:6].upper().replace(' ', '')}"
                if is_must:
                    failed_musts.append(item_id)
                    warnings.append(f"[MUST 누락] {label} — 필수 섹션 없음")
                else:
                    suggestions.append(f"[권장 추가] {label}")

        # MECE 보완 체크
        mece_checks = [
            (r"중복.*없음|no.*overlap|MECE",          "MECE 중복금지 선언"),
            (r"누락.*없음|no.*gap|Collectively",       "MECE 완전포괄 선언"),
            (r"논리.*계층|logic.*layer",               "논리 계층 유지"),
            (r"자동.*보완|auto.*補完|MECE.*체크",       "MECE 자동보완 로직"),
        ]
        mece_passed = 0
        for pat, lbl in mece_checks:
            if re.search(pat, text, re.IGNORECASE):
                mece_passed += 1
        result.mece_check_passed = mece_passed >= 3
        if not result.mece_check_passed:
            suggestions.append("[MECE 강화] MECE 자동보완 체크블록 보강 권장")

        # PE-FIN Bear Gate 정적 확인
        has_bear = bool(re.search(r"irr_bear|Bear.*Gate|Bear.*IRR", text, re.IGNORECASE))
        has_entry_ev = bool(re.search(r"ENTRY_EV|entry.?ev", text, re.IGNORECASE))
        result.irr_bear_gate = "READY" if (has_bear and has_entry_ev) else "MISSING"
        if result.irr_bear_gate == "MISSING":
            failed_musts.append("D6-IRR-BEAR")
            warnings.append("[MUST] ENTRY_EV / IRR Bear Gate 필드 미확인")

        # 총점 캡 (100점 초과 방지)
        total = min(total, TOTAL_MAX)
        result.total_score = round(total, 1)
        result.mece_dim_scores = {k: min(v, DIM_MAX[f"{k}_{'tech_structure' if k=='D1' else 'performance' if k=='D2' else 'competitive' if k=='D3' else 'operational' if k=='D4' else 'future_readiness'}"]) for k, v in dim_map.items()}
        result.industry_score = min(industry_pts, INDUSTRY_MAX)
        result.failed_must_ids = failed_musts
        result.warnings = warnings
        result.suggestions = suggestions
        result.grade = _assign_grade(result.total_score, len(failed_musts))
        result.tda_risk_level = (
            "Green"  if result.total_score >= 88 and len(failed_musts) == 0 else
            "Yellow" if result.total_score >= 65 else
            "Red"
        )
        return result


# ============================================================
# 4. 동적 채점 (--live 모드)
# ============================================================

class TDAv2Validator:
    """
    실측값 입력 기반 PE-3 동적 채점.
    D1~D5 점수 + D6 산업특화 가중치 적용 → 총점 산출.
    """

    def evaluate(self, inp: TDAv2Input) -> TDAv2Result:
        result = TDAv2Result()
        result.timestamp = datetime.now().isoformat()

        # ── D1~D5 합산 ──
        mece_dims = {
            "D1": min(inp.d1_score, DIM_MAX["D1_tech_structure"]),
            "D2": min(inp.d2_score, DIM_MAX["D2_performance"]),
            "D3": min(inp.d3_score, DIM_MAX["D3_competitive"]),
            "D4": min(inp.d4_score, DIM_MAX["D4_operational"]),
            "D5": min(inp.d5_score, DIM_MAX["D5_future_readiness"]),
        }
        mece_total = sum(mece_dims.values())

        # ── D6 산업특화 가중치 보정 ──
        weight = INDUSTRY_WEIGHT.get(inp.industry, 1.0)
        industry_weighted = min(inp.industry_raw_score * weight, INDUSTRY_MAX)
        result.industry_score = round(industry_weighted, 1)

        # ── MECE 체크 ──
        mece_checks = [
            inp.mece_no_overlap,
            inp.mece_no_gap,
            inp.mece_logic_layer,
            inp.mece_industry_add,
            inp.mece_auto_detect,
        ]
        result.mece_check_passed = sum(mece_checks) >= 4
        mece_bonus = 2.0 if result.mece_check_passed else 0.0

        # ── 총점 ──
        raw_total = mece_total + industry_weighted + mece_bonus
        result.total_score = round(min(raw_total, TOTAL_MAX), 1)
        result.mece_dim_scores = {k: round(v, 1) for k, v in mece_dims.items()}

        # ── MUST 항목 검증 ──
        failed_musts = []
        passed_musts = []

        # D3 경쟁차별화 최소 기준 (MUST: 8점 이상)
        if mece_dims["D3"] < 8:
            failed_musts.append("D3-COMPETITIVE-MUST")
            result.warnings.append("[D3 MUST] 경쟁차별화 8점 미만 — IRR 지속성 불확실")
        else:
            passed_musts.append("D3-COMPETITIVE-MUST")

        # D6 산업특화 MUST 항목
        industry_must_ids = INDUSTRY_MUST.get(inp.industry, [])
        for must_id in industry_must_ids:
            # 실측 입력에서는 industry_raw_score 기준 비례 검증
            threshold = INDUSTRY_MAX / (len(industry_must_ids) + 1)
            per_item = inp.industry_raw_score / max(len(industry_must_ids), 1)
            if per_item >= threshold * 0.7:
                passed_musts.append(must_id)
            else:
                failed_musts.append(must_id)
                result.warnings.append(f"[D6 MUST] {must_id} 미충족")

        # PE-FIN IRR Bear Gate
        if inp.irr_bear > 0:
            inp.irr_bear_gate_pass = inp.irr_bear >= inp.target_irr * 0.75
        result.irr_bear_gate = "PASS" if inp.irr_bear_gate_pass else "FAIL"
        if result.irr_bear_gate == "FAIL":
            failed_musts.append("D6-IRR-BEAR-GATE")
            result.warnings.append(
                f"[IRR Bear Gate FAIL] Bear IRR {inp.irr_bear:.1f}% < "
                f"목표 {inp.target_irr:.1f}% × 75% = {inp.target_irr*0.75:.1f}%"
            )
        else:
            passed_musts.append("D6-IRR-BEAR-GATE")

        result.failed_must_ids = failed_musts
        result.passed_must_ids = passed_musts

        # ── 등급 판정 ──
        result.grade = _assign_grade(result.total_score, len(failed_musts))
        result.tda_risk_level = inp.tda_risk_level if inp.tda_risk_level else (
            "Green"  if result.total_score >= 88 and len(failed_musts) == 0 else
            "Yellow" if result.total_score >= 65 else
            "Red"
        )

        # ── 개선 제안 ──
        if mece_dims["D4"] < 10:
            result.suggestions.append("D4 운영실행 보강 권장 — Key Person Risk / 기술부채 구체화")
        if mece_dims["D5"] < 10:
            result.suggestions.append("D5 미래대응 보강 권장 — 규제 리스크 / 3~10년 시나리오 추가")
        if result.industry_score < 12:
            result.suggestions.append(f"D6 {inp.industry} 특화 보강 — 산업 MUST 항목 구체화 필요")

        return result


# ============================================================
# 5. 공통 등급 판정 함수
# ============================================================

def _assign_grade(score: float, failed_must_count: int) -> str:
    for min_score, max_must, grade in GRADE_TABLE:
        if score >= min_score and failed_must_count <= max_must:
            return grade
    return "D"


# ============================================================
# 6. Notion 19필드 자동기록
# ============================================================

def write_to_notion(
    page_id: str,
    inp:      TDAv2Input,
    result:   TDAv2Result,
    dry_run:  bool = False
) -> None:
    """PE-TDA v2.0 결과 → Notion 19필드 자동기록"""

    props = {
        # ─ PE-3 채점 결과 (6필드) ─
        "PE3 Grade":          {"rich_text": [{"text": {"content": result.grade}}]},
        "PE3 Score":          {"number": result.total_score},
        "PE3 Failed Must":    {"rich_text": [{"text": {"content": ", ".join(result.failed_must_ids) or "없음"}}]},
        "D6 Industry Layer":  {"rich_text": [{"text": {"content": inp.industry}}]},
        "Analysis Mode":      {"rich_text": [{"text": {"content": inp.analysis_mode}}]},
        "Analysis Depth":     {"rich_text": [{"text": {"content": inp.analysis_depth}}]},

        # ─ MECE D1~D5 차원 점수 (5필드) ─
        "D1 Score":           {"number": result.mece_dim_scores.get("D1", 0)},
        "D2 Score":           {"number": result.mece_dim_scores.get("D2", 0)},
        "D3 Score":           {"number": result.mece_dim_scores.get("D3", 0)},
        "D4 Score":           {"number": result.mece_dim_scores.get("D4", 0)},
        "D5 Score":           {"number": result.mece_dim_scores.get("D5", 0)},

        # ─ D6 산업특화 & 리스크 (2필드) ─
        "D6 Industry Score":  {"number": result.industry_score},
        "TDA Risk Level":     {"select": {"name": result.tda_risk_level}},

        # ─ PE-FIN IRR 연동 (4필드) ─
        "Entry EV":           {"number": inp.entry_ev},
        "IRR Entry EV Cap":   {"number": inp.irr_entry_ev_cap},
        "IRR Bear":           {"number": inp.irr_bear},
        "IRR Result":         {"number": inp.irr_base},

        # ─ 운영 메타 (2필드) ─
        "Key Insight":        {"rich_text": [{"text": {"content": inp.key_insight[:2000] if inp.key_insight else ""}}]},
        "Deliverable URL":    {"url": inp.deliverable_url if inp.deliverable_url else None},
    }

    # URL None 필드 제거
    if props["Deliverable URL"]["url"] is None:
        del props["Deliverable URL"]

    if dry_run:
        print("\n[DRY-RUN] Notion 19필드 Payload:")
        print(json.dumps(props, ensure_ascii=False, indent=2))
        return

    if NotionClient is None:
        print("[ERROR] notion-client 미설치: pip install notion-client")
        sys.exit(1)

    token = os.environ.get("NOTION_TOKEN")
    if not token:
        print("[ERROR] 환경변수 NOTION_TOKEN 미설정")
        sys.exit(1)

    notion = NotionClient(auth=token)
    notion.pages.update(page_id=page_id, properties=props)
    print(f"[OK] Notion {page_id} — 19필드 업데이트 완료")


# ============================================================
# 7. 리포트 출력
# ============================================================

GRADE_EMOJI = {
    "A+": "🟣", "A": "🔵", "B+": "🟢",
    "B":  "🟡", "C":  "🟠", "D":  "🔴",
}
RISK_EMOJI = {"Green": "🟢", "Yellow": "🟡", "Red": "🔴"}


def print_report(inp_or_path, result: TDAv2Result, mode: str = "live") -> None:
    emoji = GRADE_EMOJI.get(result.grade, "⚪")
    risk  = RISK_EMOJI.get(result.tda_risk_level, "⚪")

    print("\n" + "═" * 65)
    print(f"  PE-TDA v2.0  PE-3 채점 결과")
    print(f"  {emoji} {result.grade}등급  |  총점: {result.total_score}/100  |  리스크: {risk} {result.tda_risk_level}")
    print(f"  모드: {mode.upper()}  |  IRR Bear Gate: {result.irr_bear_gate}")
    print("═" * 65)

    print("\n[MECE 5차원 점수]  (각 최대 16점, 합계 80점)")
    dim_labels = {
        "D1": "D1 기술구조    ",
        "D2": "D2 성능·확장성 ",
        "D3": "D3 경쟁 차별화 ",
        "D4": "D4 운영 실행   ",
        "D5": "D5 미래 대응   ",
    }
    for k, lbl in dim_labels.items():
        s = result.mece_dim_scores.get(k, 0)
        bar = "█" * int(s) + "░" * (16 - int(s))
        print(f"  {lbl}: {s:5.1f}  [{bar}]")

    print(f"\n[D6 산업특화 점수]  (최대 20점)")
    industry = inp_or_path.industry if hasattr(inp_or_path, 'industry') else 'N/A'
    s6 = result.industry_score
    bar6 = "█" * int(s6) + "░" * (20 - int(s6))
    print(f"  {industry:15s}: {s6:5.1f}  [{bar6}]")

    mece_total = sum(result.mece_dim_scores.values())
    print(f"\n  MECE D1~D5 합계 : {mece_total:5.1f} / 80")
    print(f"  D6 산업특화      : {result.industry_score:5.1f} / 20")
    print(f"  ─────────────────────────────")
    print(f"  총점             : {result.total_score:5.1f} / 100")

    print(f"\n[MECE 자동보완] {'✅ PASS' if result.mece_check_passed else '❌ FAIL — 보완 필요'}")

    if result.failed_must_ids:
        print(f"\n[MUST 미통과] → {', '.join(result.failed_must_ids)}")
    else:
        print("\n[MUST] 전항목 통과 ✅")

    if result.passed_must_ids:
        print(f"[MUST 통과] → {', '.join(result.passed_must_ids)}")

    if result.warnings:
        print("\n[경고]")
        for w in result.warnings:
            print(f"  ⚠️  {w}")

    if result.suggestions:
        print("\n[개선 제안]")
        for s in result.suggestions:
            print(f"  💡 {s}")

    print("\n" + "═" * 65)


# ============================================================
# 8. CLI 진입점
# ============================================================

def parse_args():
    p = argparse.ArgumentParser(
        description="PE-TDA v2.0 PE-3 자동채점 엔진",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    # 실행 모드
    mode_group = p.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--file",           metavar="PATH", help="프롬프트 .md 파일 정적 분석")
    mode_group.add_argument("--live",           action="store_true", help="실측값 기반 동적 채점")
    mode_group.add_argument("--revalidate-all", action="store_true", help="PE-TDA 전체 레코드 배치 재검증")
    mode_group.add_argument("--pe3-dashboard",  action="store_true", help="PE-3 현황 대시보드 출력")

    # 공통
    p.add_argument("--page-id",       type=str,   default="",    help="Notion 페이지 ID")
    p.add_argument("--target-score",  type=float, default=95.0,  help="목표 PE-3 점수 (기본 95)")
    p.add_argument("--qc-strict",     action="store_true",        help="MUST 미통과 시 비정상 종료")
    p.add_argument("--dry-run",       action="store_true",        help="Notion 기록 건너뜀")

    # --live 모드 전용
    p.add_argument("--industry",      type=str,   default="AI")
    p.add_argument("--mode",          type=str,   default="Investment")
    p.add_argument("--depth",         type=str,   default="Strategic")
    p.add_argument("--tech-name",     type=str,   default="")
    p.add_argument("--company",       type=str,   default="")

    # D1~D5 점수
    p.add_argument("--d1-score",      type=float, default=0.0)
    p.add_argument("--d2-score",      type=float, default=0.0)
    p.add_argument("--d3-score",      type=float, default=0.0)
    p.add_argument("--d4-score",      type=float, default=0.0)
    p.add_argument("--d5-score",      type=float, default=0.0)
    p.add_argument("--industry-score",type=float, default=0.0)

    # MECE 체크
    p.add_argument("--mece-no-overlap",  action="store_true")
    p.add_argument("--mece-no-gap",      action="store_true")
    p.add_argument("--mece-logic-layer", action="store_true")
    p.add_argument("--mece-industry-add",action="store_true")
    p.add_argument("--mece-auto-detect", action="store_true")

    # PE-FIN IRR
    p.add_argument("--irr-base",      type=float, default=0.0)
    p.add_argument("--irr-bear",      type=float, default=0.0)
    p.add_argument("--entry-ev",      type=float, default=0.0)
    p.add_argument("--irr-ev-cap",    type=float, default=0.0)
    p.add_argument("--target-irr",    type=float, default=20.0)
    p.add_argument("--irr-sensitivity",action="store_true")
    p.add_argument("--irr-bear-gate", action="store_true")

    # 운영
    p.add_argument("--risk-level",    type=str,   default="Yellow")
    p.add_argument("--key-insight",   type=str,   default="")
    p.add_argument("--deliverable-url",type=str,  default="")

    return p.parse_args()


def main():
    args = parse_args()

    # ── --file 모드 ──
    if args.file:
        analyzer = PromptStaticAnalyzer()
        result   = analyzer.analyze(args.file)
        print_report(type('F', (), {'industry': 'N/A'})(), result, mode="static")

        if args.target_score and result.total_score < args.target_score:
            print(f"\n[QC] 목표 점수 {args.target_score}점 미달 (현재: {result.total_score}점)")
            if args.qc_strict:
                sys.exit(1)
        if args.qc_strict and result.failed_must_ids:
            print(f"[QC-STRICT] MUST 미통과 — 종료: {result.failed_must_ids}")
            sys.exit(1)
        print(f"\n[QC] 정적 분석 완료 | 파일: {args.file}")
        return

    # ── --live 모드 ──
    if args.live:
        inp = TDAv2Input(
            tech_name=args.tech_name,
            company=args.company,
            industry=args.industry,
            analysis_mode=args.mode,
            analysis_depth=args.depth,
            d1_score=args.d1_score,
            d2_score=args.d2_score,
            d3_score=args.d3_score,
            d4_score=args.d4_score,
            d5_score=args.d5_score,
            industry_raw_score=args.industry_score,
            mece_no_overlap=args.mece_no_overlap,
            mece_no_gap=args.mece_no_gap,
            mece_logic_layer=args.mece_logic_layer,
            mece_industry_add=args.mece_industry_add,
            mece_auto_detect=args.mece_auto_detect,
            irr_base=args.irr_base,
            irr_bear=args.irr_bear,
            entry_ev=args.entry_ev,
            irr_entry_ev_cap=args.irr_ev_cap,
            target_irr=args.target_irr,
            irr_bear_gate_pass=args.irr_bear_gate,
            irr_sensitivity_ok=args.irr_sensitivity,
            tda_risk_level=args.risk_level,
            key_insight=args.key_insight,
            deliverable_url=args.deliverable_url,
            notion_page_id=args.page_id,
        )
        validator = TDAv2Validator()
        result    = validator.evaluate(inp)
        print_report(inp, result, mode="live")

        if args.page_id:
            write_to_notion(args.page_id, inp, result, dry_run=args.dry_run)

        if args.qc_strict and result.failed_must_ids:
            print(f"[QC-STRICT] MUST 미통과 — 종료: {result.failed_must_ids}")
            sys.exit(1)
        return

    # ── --revalidate-all 모드 ──
    if args.revalidate_all:
        print("[REVALIDATE-ALL] PE-TDA 전체 레코드 재검증 — pe7_tda_loop.py와 연계하여 실행하세요.")
        print("  python automation/pe7_tda_loop.py --revalidate-all --qc-strict")
        return

    # ── --pe3-dashboard 모드 ──
    if args.pe3_dashboard:
        print("[PE-3 DASHBOARD] 전체 도메인 현황 — pe7_tda_loop.py와 연계하여 실행하세요.")
        print("  python automation/pe7_tda_loop.py --pe3-dashboard")
        return


if __name__ == "__main__":
    main()
