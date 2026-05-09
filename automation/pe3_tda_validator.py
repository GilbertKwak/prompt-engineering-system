#!/usr/bin/env python3
"""
pe3_tda_validator.py — PE-TDA (Technology & Deal Assessment) QC 검증 엔진
Version : 1.0 | Date: 2026-05-09
Author  : Gilbert

도메인 정의 (MECE 경계 v1.0):
  PE-TDA = 기술실사(Tech DD) + 딜 구조 적정성 검증
           → 「기술 완성도 × 딜 조건 교차 검증」이 핵심
  PE-DD  = 재무/법무/운영 실사 (비기술 영역)
           → 두 도메인의 교차점 = IP 가치평가 (공유 체크)

검증 차원 (D1~D7):
  D1  기술 성숙도 (TRL 평가)
  D2  IP 포트폴리오 & 방어력
  D3  기술 로드맵 실현 가능성
  D4  딜 구조 & 밸류에이션 적정성
  D5  팀 역량 & 실행력
  D6  리스크 매트릭스 (기술 × 딜)
  D7  Cross-Library 태깅 정합성

사용법:
  python pe3_tda_validator.py --file <분석결과.md>
  python pe3_tda_validator.py --file <f.md> --strict
  python pe3_tda_validator.py --file <f.md> --domain-check   # DD/TDA 혼용 감지
  python pe3_tda_validator.py --boundary                     # MECE 경계 요약 출력
"""

import argparse
import re
import sys
from pathlib import Path

# ── 버전 ────────────────────────────────────────────────────────────────────
VERSION = "1.0"
STRICT_THRESHOLD = 88.0

# ── TDA 체크 정의 (D1~D7) ────────────────────────────────────────────────────
# 구조: {id, name, dimension, level, patterns(OR 조건), negative_patterns(NG)}
BUILTIN_CHECKS = [

    # ── D1: 기술 성숙도 (TRL) ─────────────────────────────────────────────
    {
        "id": "TDA-D1-01",
        "name": "TRL 레벨 명시",
        "dimension": "D1",
        "dimension_name": "기술 성숙도",
        "level": "MUST",
        "patterns": [r"TRL[\s\-]*[1-9]", r"기술성숙도[\s:]*[1-9]"],
        "negative_patterns": [],
        "weight": 15,
    },
    {
        "id": "TDA-D1-02",
        "name": "TRL 갭 분석 (현재→목표)",
        "dimension": "D1",
        "dimension_name": "기술 성숙도",
        "level": "MUST",
        "patterns": [r"TRL[^\n]*→", r"TRL[^\n]*현재[^\n]*목표", r"TRL[^\n]*Gap"],
        "negative_patterns": [],
        "weight": 12,
    },
    {
        "id": "TDA-D1-03",
        "name": "기술 차별화 근거 (벤치마크 vs 경쟁사)",
        "dimension": "D1",
        "dimension_name": "기술 성숙도",
        "level": "SHOULD",
        "patterns": [r"벤치마크", r"benchmark", r"경쟁사 대비", r"vs\s+[A-Z]"],
        "negative_patterns": [],
        "weight": 8,
    },

    # ── D2: IP 포트폴리오 ──────────────────────────────────────────────────
    {
        "id": "TDA-D2-01",
        "name": "특허 건수 및 등록 상태 명시",
        "dimension": "D2",
        "dimension_name": "IP 포트폴리오",
        "level": "MUST",
        "patterns": [r"특허[^\n]*[0-9]+건", r"patent[^\n]*[0-9]+",
                     r"등록특허", r"출원특허"],
        "negative_patterns": [],
        "weight": 14,
    },
    {
        "id": "TDA-D2-02",
        "name": "IP 방어력 평가 (회피설계 가능성)",
        "dimension": "D2",
        "dimension_name": "IP 포트폴리오",
        "level": "MUST",
        "patterns": [r"회피설계", r"design.around", r"IP 방어",
                     r"특허 분쟁", r"침해 리스크"],
        "negative_patterns": [],
        "weight": 12,
    },
    {
        "id": "TDA-D2-03",
        "name": "IP 가치평가 방법론 (원가/수익/시장)",
        "dimension": "D2",
        "dimension_name": "IP 포트폴리오",
        "level": "SHOULD",
        "patterns": [r"IP 가치평가", r"로열티", r"royalt",
                     r"원가법", r"수익접근법", r"시장접근법"],
        "negative_patterns": [],
        "weight": 8,
    },

    # ── D3: 기술 로드맵 실현 가능성 ───────────────────────────────────────
    {
        "id": "TDA-D3-01",
        "name": "마일스톤 3개 이상 (날짜 or 분기 기재)",
        "dimension": "D3",
        "dimension_name": "로드맵 실현가능성",
        "level": "MUST",
        "patterns": [r"Phase\s*[123]", r"마일스톤[^\n]*[0-9]{4}",
                     r"Q[1-4]\s*[0-9]{4}", r"[0-9]+개월"],
        "negative_patterns": [],
        "weight": 12,
    },
    {
        "id": "TDA-D3-02",
        "name": "기술 리스크 병목 식별",
        "dimension": "D3",
        "dimension_name": "로드맵 실현가능성",
        "level": "MUST",
        "patterns": [r"기술 리스크", r"병목", r"bottleneck",
                     r"Critical Path", r"단일 실패점"],
        "negative_patterns": [],
        "weight": 10,
    },
    {
        "id": "TDA-D3-03",
        "name": "외부 의존성 (부품/공급망/라이선스)",
        "dimension": "D3",
        "dimension_name": "로드맵 실현가능성",
        "level": "SHOULD",
        "patterns": [r"공급망", r"supply.chain", r"외부 의존",
                     r"라이선스 의존", r"TSMC|삼성파운드리|ASML"],
        "negative_patterns": [],
        "weight": 7,
    },

    # ── D4: 딜 구조 & 밸류에이션 ──────────────────────────────────────────
    {
        "id": "TDA-D4-01",
        "name": "Entry EV / Pre-Money 밸류에이션 명시",
        "dimension": "D4",
        "dimension_name": "딜 구조 & 밸류",
        "level": "MUST",
        "patterns": [r"Entry EV", r"Pre.Money", r"밸류에이션[^\n]*[0-9]",
                     r"기업가치[^\n]*[0-9]"],
        "negative_patterns": [],
        "weight": 15,
    },
    {
        "id": "TDA-D4-02",
        "name": "딜 조건 핵심 3요소 (지분율/조건부/Exit)",
        "dimension": "D4",
        "dimension_name": "딜 구조 & 밸류",
        "level": "MUST",
        "patterns": [r"지분율", r"조건부 전환", r"Ratchet",
                     r"Exit.*Multiple", r"우선청산권"],
        "negative_patterns": [],
        "weight": 13,
    },
    {
        "id": "TDA-D4-03",
        "name": "밸류에이션 멀티플 근거 (섹터 Comp)",
        "dimension": "D4",
        "dimension_name": "딜 구조 & 밸류",
        "level": "SHOULD",
        "patterns": [r"Comp[^a-z]", r"Comparable", r"섹터 평균",
                     r"EV/EBITDA", r"P/S"],
        "negative_patterns": [],
        "weight": 8,
    },

    # ── D5: 팀 역량 ────────────────────────────────────────────────────────
    {
        "id": "TDA-D5-01",
        "name": "핵심 인력 이탈 리스크 평가",
        "dimension": "D5",
        "dimension_name": "팀 역량 & 실행력",
        "level": "MUST",
        "patterns": [r"핵심 인력", r"Key Man", r"인력 이탈",
                     r"의존도.*CTO|CTO.*의존"],
        "negative_patterns": [],
        "weight": 12,
    },
    {
        "id": "TDA-D5-02",
        "name": "기술 인력 채용 계획 (충원 시점 포함)",
        "dimension": "D5",
        "dimension_name": "팀 역량 & 실행력",
        "level": "SHOULD",
        "patterns": [r"채용 계획", r"인력 충원", r"Hiring Plan",
                     r"R&D 헤드카운트"],
        "negative_patterns": [],
        "weight": 7,
    },

    # ── D6: 리스크 매트릭스 ────────────────────────────────────────────────
    {
        "id": "TDA-D6-01",
        "name": "기술 리스크 × 딜 리스크 교차 매트릭스",
        "dimension": "D6",
        "dimension_name": "리스크 매트릭스",
        "level": "MUST",
        "patterns": [r"리스크[^\n]*매트릭스", r"Risk.*Matrix",
                     r"확률.*영향도", r"[H/M/L].*리스크"],
        "negative_patterns": [],
        "weight": 14,
    },
    {
        "id": "TDA-D6-02",
        "name": "Downside 시나리오 (Bear Case) 정량화",
        "dimension": "D6",
        "dimension_name": "리스크 매트릭스",
        "level": "MUST",
        "patterns": [r"Bear[^\n]*Case", r"Downside[^\n]*[0-9]",
                     r"최악.*시나리오", r"Bear IRR"],
        "negative_patterns": [],
        "weight": 12,
    },
    {
        "id": "TDA-D6-03",
        "name": "규제/인증 리스크 (FDA/CE/KC 등)",
        "dimension": "D6",
        "dimension_name": "리스크 매트릭스",
        "level": "SHOULD",
        "patterns": [r"FDA", r"CE 인증", r"KC", r"인허가",
                     r"규제 리스크", r"인증 일정"],
        "negative_patterns": [],
        "weight": 6,
    },

    # ── D7: Cross-Library 태깅 정합성 ─────────────────────────────────────
    {
        "id": "TDA-D7-01",
        "name": "PE-TDA 도메인 태그 존재",
        "dimension": "D7",
        "dimension_name": "Cross-Library 태깅",
        "level": "MUST",
        "patterns": [r"PE-TDA"],
        "negative_patterns": [],
        "weight": 10,
    },
    {
        "id": "TDA-D7-02",
        "name": "PE-DD 혼용 없음 (재무/법무 실사 내용 미포함)",
        "dimension": "D7",
        "dimension_name": "Cross-Library 태깅",
        "level": "SHOULD",
        "patterns": [r"(?!.*재무실사)(?!.*법무실사)(?!.*PE-DD)."],
        # PE-DD 전용 키워드가 있으면 경고 (negative)
        "negative_patterns": [r"재무실사", r"법무실사",
                               r"감사보고서 검토", r"계약서 리뷰"],
        "weight": 5,
    },
    {
        "id": "TDA-D7-03",
        "name": "IP 가치평가는 PE-TDA/PE-DD 공유 체크 명시",
        "dimension": "D7",
        "dimension_name": "Cross-Library 태깅",
        "level": "SHOULD",
        "patterns": [r"IP 가치평가", r"IP Valuation",
                     r"지식재산 가치"],
        "negative_patterns": [],
        "weight": 5,
    },
]

# 차원별 메타
DIMENSION_META = {
    "D1": {"name": "기술 성숙도",         "weight": 20},
    "D2": {"name": "IP 포트폴리오",        "weight": 18},
    "D3": {"name": "로드맵 실현가능성",    "weight": 15},
    "D4": {"name": "딜 구조 & 밸류",       "weight": 20},
    "D5": {"name": "팀 역량 & 실행력",     "weight": 10},
    "D6": {"name": "리스크 매트릭스",      "weight": 12},
    "D7": {"name": "Cross-Library 태깅",  "weight":  5},
}


# ── 핵심 검증 엔진 ────────────────────────────────────────────────────────────

def load_checks(yaml_path: str = None) -> list:
    """YAML 체크리스트 로드 (없으면 BUILTIN 반환)."""
    if yaml_path:
        try:
            import yaml
            with open(yaml_path, encoding="utf-8") as f:
                data = yaml.safe_load(f)
            return data.get("checks", BUILTIN_CHECKS)
        except Exception:
            pass
    return BUILTIN_CHECKS


def _check_one(chk: dict, text: str) -> bool:
    """단일 체크 실행. negative_patterns 중 하나라도 매칭 시 False."""
    for neg in chk.get("negative_patterns", []):
        if re.search(neg, text, re.IGNORECASE):
            return False
    for pat in chk.get("patterns", []):
        if re.search(pat, text, re.IGNORECASE | re.DOTALL):
            return True
    return False


def validate(text: str, checks: list = None) -> dict:
    """
    TDA 분석 텍스트를 D1~D7로 검증.

    반환:
      overall   : 0~100 가중 합산 점수
      grade     : S/A/B/C/D 등급
      dimensions: {D1: {name, score, max, pct, checks:[...]}, ...}
    """
    if checks is None:
        checks = BUILTIN_CHECKS

    dim_results = {d: {"name": m["name"], "score": 0, "max": 0,
                       "checks": []}
                   for d, m in DIMENSION_META.items()}

    for chk in checks:
        d = chk["dimension"]
        passed = _check_one(chk, text)
        w = chk["weight"]
        dim_results[d]["max"] += w
        if passed:
            dim_results[d]["score"] += w
        dim_results[d]["checks"].append({
            "id":     chk["id"],
            "name":   chk["name"],
            "level":  chk["level"],
            "passed": passed,
            "weight": w,
        })

    # 차원별 달성률 계산
    for d, dr in dim_results.items():
        dr["pct"] = round(100 * dr["score"] / dr["max"], 1) if dr["max"] else 0

    # 가중 Overall
    total_w = sum(m["weight"] for m in DIMENSION_META.values())
    overall = sum(
        dim_results[d]["pct"] * DIMENSION_META[d]["weight"] / total_w
        for d in DIMENSION_META
    )
    overall = round(overall, 1)

    # 등급
    if overall >= 95:  grade = "S — 투자 즉시 진행 권고"
    elif overall >= 88: grade = "A — 투자 권고 (경미한 보완)"
    elif overall >= 78: grade = "B — 조건부 투자 (보완 필요)"
    elif overall >= 65: grade = "C — 재실사 권고"
    else:               grade = "D — 투자 보류"

    return {"overall": overall, "grade": grade, "dimensions": dim_results}


# ── PE-DD / PE-TDA MECE 경계 감지 ────────────────────────────────────────────

# PE-DD 전용 키워드 (TDA 문서에 있으면 혼용 경고)
_DD_ONLY_PATTERNS = [
    (r"감사보고서",    "재무실사(PE-DD) 키워드"),
    (r"법무실사",      "법무실사(PE-DD) 키워드"),
    (r"계약서\s*리뷰", "계약서 검토(PE-DD) 키워드"),
    (r"우발채무",      "우발채무(PE-DD) 키워드"),
    (r"세무조정",      "세무(PE-DD) 키워드"),
    (r"노무\s*실사",   "노무실사(PE-DD) 키워드"),
]

# PE-TDA 전용 키워드 (DD 문서에 있으면 혼용 경고)
_TDA_ONLY_PATTERNS = [
    (r"TRL\s*[0-9]",  "TRL 레벨(PE-TDA) 키워드"),
    (r"회피설계",      "IP 방어(PE-TDA) 키워드"),
    (r"기술 성숙도",   "기술성숙도(PE-TDA) 키워드"),
    (r"기술 로드맵",   "기술로드맵(PE-TDA) 키워드"),
]


def domain_check(text: str, declared_domain: str = "PE-TDA") -> dict:
    """
    선언된 도메인(PE-TDA 또는 PE-DD) 기준으로
    상대 도메인 키워드 혼용 여부를 검사.
    """
    warnings = []
    if declared_domain == "PE-TDA":
        for pat, label in _DD_ONLY_PATTERNS:
            if re.search(pat, text, re.IGNORECASE):
                warnings.append(f"[혼용경고] {label} 감지 → PE-DD로 분리 권고")
    else:  # PE-DD
        for pat, label in _TDA_ONLY_PATTERNS:
            if re.search(pat, text, re.IGNORECASE):
                warnings.append(f"[혼용경고] {label} 감지 → PE-TDA로 분리 권고")
    return {
        "declared": declared_domain,
        "warnings": warnings,
        "clean": len(warnings) == 0,
    }


# ── CLI ────────────────────────────────────────────────────────────────────────

BOUNDARY_TEXT = """
╔══════════════════════════════════════════════════════════════╗
║         PE-TDA vs PE-DD  MECE 경계 정의 v1.0                ║
╠══════════════════════════════════════════════════════════════╣
║  PE-TDA  기술실사 + 딜 구조 검증                             ║
║  ────────────────────────────────────────────────            ║
║  ● TRL 레벨 평가 (D1)                                        ║
║  ● IP 포트폴리오 & 방어력 (D2)  ← 공유: IP 가치평가         ║
║  ● 기술 로드맵 실현가능성 (D3)                               ║
║  ● 딜 구조 & 밸류에이션 (D4)   ← 공유: Entry EV 적정성      ║
║  ● 팀/기술 역량 (D5)                                         ║
║  ● 기술×딜 리스크 매트릭스 (D6)                              ║
║  ● Cross-Library 태깅 (D7)                                   ║
╠══════════════════════════════════════════════════════════════╣
║  PE-DD   비기술 실사 (재무/법무/운영)                        ║
║  ────────────────────────────────────────────────            ║
║  ● 감사보고서 & 재무제표 분석                                ║
║  ● 법무실사 (계약/소송/규정)                                 ║
║  ● 세무 & 우발채무                                           ║
║  ● 노무/HR 실사                                              ║
║  ● IP 가치평가 방법론          ← 공유: TDA-D2와 중복 허용   ║
║  ● Entry EV 적정성 검토        ← 공유: TDA-D4와 중복 허용   ║
╠══════════════════════════════════════════════════════════════╣
║  공유 영역 (Cross-Library 이중 태깅 필수)                    ║
║  → IP 가치평가 / Entry EV 적정성 / Bear Case IRR             ║
║  → 태깅 규칙: [PE-TDA, PE-DD] 동시 기재                     ║
╚══════════════════════════════════════════════════════════════╝
"""


def qc_only_mode(file_path: str, strict: bool = False,
                 domain_flag: bool = False,
                 yaml_path: str = None) -> int:
    content = Path(file_path).read_text(encoding="utf-8")
    print(f"\n🔬 PE-TDA QC — {Path(file_path).name}")

    checks = load_checks(yaml_path)
    result = validate(content, checks)
    overall = result["overall"]

    bar_filled = int(overall / 5)
    bar = "█" * bar_filled + "░" * (20 - bar_filled)
    print(f"\n  Overall : [{bar}] {overall:.1f}%  {result['grade']}")

    sep = "─" * 58
    print(f"  {sep}")
    print(f"  {'차원':<22} {'점수':>6} {'달성률':>8}  그래프")
    print(f"  {sep}")
    for d_id, dr in sorted(result["dimensions"].items()):
        b2 = "█" * int(dr["pct"] / 5) + "░" * (20 - int(dr["pct"] / 5))
        print(f"  {d_id} {dr['name']:<18} "
              f"{dr['score']:>3}/{dr['max']:<3} "
              f"{dr['pct']:>6.1f}%  [{b2}]")
    print(f"  {sep}")

    # MUST 미충족
    failed_must = [
        f"{c['id']}: {c['name']}"
        for dr in result["dimensions"].values()
        for c in dr["checks"]
        if c["level"] == "MUST" and not c["passed"]
    ]
    if failed_must:
        print(f"\n  ⚠️  MUST 미충족 ({len(failed_must)}건):")
        for item in failed_must:
            print(f"      ✘ {item}")
    else:
        print("\n  ✅ 모든 MUST 항목 통과")

    # 도메인 경계 체크
    if domain_flag:
        dc = domain_check(content, "PE-TDA")
        print(f"\n  🔍 도메인 경계 감지 ({'CLEAN' if dc['clean'] else 'WARN'})")
        for w in dc["warnings"]:
            print(f"      ⚡ {w}")
        if dc["clean"]:
            print("      ✅ PE-DD 혼용 키워드 없음")

    print()
    if strict and overall < STRICT_THRESHOLD:
        print(f"  🛑 STRICT 모드: {overall:.1f}% < {STRICT_THRESHOLD}% — 실패")
        return 1
    return 0


def main():
    parser = argparse.ArgumentParser(
        description=f"PE-TDA QC 검증 엔진 v{VERSION}"
    )
    parser.add_argument("--file",         help="검증할 마크다운 파일")
    parser.add_argument("--strict",        action="store_true",
                        help=f"{STRICT_THRESHOLD}점 미만 시 exit(1)")
    parser.add_argument("--domain-check",  action="store_true",
                        help="PE-DD 혼용 키워드 감지")
    parser.add_argument("--boundary",      action="store_true",
                        help="PE-TDA vs PE-DD MECE 경계 요약 출력")
    parser.add_argument("--yaml",          help="커스텀 YAML 체크리스트 경로")
    args = parser.parse_args()

    if args.boundary:
        print(BOUNDARY_TEXT)
        return

    if not args.file:
        parser.print_help()
        sys.exit(1)

    sys.exit(qc_only_mode(
        args.file,
        strict=args.strict,
        domain_flag=args.domain_check,
        yaml_path=args.yaml,
    ))


if __name__ == "__main__":
    main()
