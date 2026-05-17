#!/usr/bin/env python3
"""
automation/vc_layer_router.py
PE-VC-02 / PE-VC-03 계층적 선택 적용 라우터

Layer 2 (PE-VC-02): 전 도메인 전처리 게이트
Layer 3 (PE-VC-03): PE-AI-ECO / PE-SEMI / PE-DD 3종 심층 적용
"""

import re
import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

# ──────────────────────────────────────────────
# 상수 정의
# ──────────────────────────────────────────────

# Layer 3 심층 적용 도메인 (3종 고정)
LAYER3_DOMAINS = {"PE-AI-ECO", "PE-SEMI", "PE-DD"}

# Intent Class → 우선 도메인 매핑
INTENT_DOMAIN_MAP = {
    "A": ["PE-SEMI", "PE-MIN", "PE-AI-ECO"],   # 시장분석/경쟁정보
    "B": ["PE-FIN", "PE-DD"],                   # 재무모델링/밸류에이션
    "C": ["PE-STRAT", "PE-NBD"],               # 전략수립/의사결정
    "D": ["PE-SEMI", "PE-TDA", "PE-THERM"],    # 기술분석/설계
    "E": ["PE-AI-ECO", "PE-SEMI", "PE-DD"],    # 복합/크로스도메인 → L3
}

# 약어 확장 사전
ABBREV_MAP = {
    "HBM": "High Bandwidth Memory (HBM)",
    "CoWoS": "Chip-on-Wafer-on-Substrate (CoWoS)",
    "TSMC": "TSMC (Taiwan Semiconductor Manufacturing Company)",
    "AI": "Artificial Intelligence (AI)",
    "DD": "Due Diligence (DD)",
    "VC": "Venture Capital / Valuation Check (VC)",
    "SEMI": "Semiconductor (SEMI)",
    "CAPEX": "Capital Expenditure (CAPEX)",
    "EBITDA": "Earnings Before Interest Taxes Depreciation & Amortization (EBITDA)",
    "GNN": "Graph Neural Network (GNN)",
    "GraphSAGE": "Graph Sample and Aggregation (GraphSAGE)",
}

# Layer 3 에스컬레이션 키워드
LAYER3_KEYWORDS = {
    "PE-AI-ECO": ["밸류체인", "생태계", "전방위", "value chain", "ecosystem", "AI stack"],
    "PE-SEMI": ["공급망 충격", "shock", "시뮬레이션", "GNN", "GraphSAGE", "HHI", "SMIC"],
    "PE-DD": ["리스크 스코어", "risk score", "밸류에이션", "valuation", "governance", "거버넌스"],
}


# ──────────────────────────────────────────────
# 데이터 클래스
# ──────────────────────────────────────────────

@dataclass
class RoutingPacket:
    normalized_query: str
    intent_class: str
    primary_domain: str
    context_injected: bool
    layer3_escalate: bool
    layer3_modules: list = field(default_factory=list)
    format_spec: dict = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))

    def to_dict(self):
        return {
            "preprocess": {
                "normalized_query": self.normalized_query,
                "intent_class": self.intent_class,
                "primary_domain": self.primary_domain,
                "context_injected": self.context_injected,
                "layer3_escalate": self.layer3_escalate,
                "layer3_modules": self.layer3_modules,
                "format_spec": self.format_spec,
                "timestamp": self.timestamp,
            }
        }

    def to_yaml_str(self):
        d = self.to_dict()["preprocess"]
        lines = ["# PE-VC-02 라우팅 패킷"]
        lines.append("preprocess:")
        for k, v in d.items():
            if isinstance(v, list):
                lines.append(f"  {k}:")
                for item in v:
                    lines.append(f"    - {item}")
            elif isinstance(v, dict):
                lines.append(f"  {k}:")
                for dk, dv in v.items():
                    lines.append(f"    {dk}: {dv}")
            else:
                lines.append(f"  {k}: {str(v)}")
        return "\n".join(lines)


# ──────────────────────────────────────────────
# Layer 2 — 전처리 게이트
# ──────────────────────────────────────────────

def normalize_query(query: str) -> str:
    """STAGE 1: 쿼리 정규화"""
    fillers = ["좀", "한번", "빠르게", "그냥", "약간", "대충"]
    result = query.strip()
    for f in fillers:
        result = result.replace(f, "")
    result = re.sub(r" {2,}", " ", result).strip()
    return result


def classify_intent(query: str, domain: Optional[str] = None) -> str:
    """STAGE 2: 의도 분류"""
    q = query.lower()

    # 복합 크로스도메인 키워드
    cross_domain = ["밸류체인 전반", "전방위", "생태계 전체", "공급망 + 재무", "cross-domain"]
    if any(kw in q for kw in cross_domain):
        return "E"

    # 재무/밸류에이션
    fin_kw = ["재무", "밸류에이션", "valuation", "dcf", "ebitda", "irr", "npv", "dd", "due diligence"]
    if any(kw in q for kw in fin_kw):
        return "B"

    # 기술분석
    tech_kw = ["공정", "nm", "euvl", "gnn", "그래프", "열특성", "thermal", "설계", "architecture"]
    if any(kw in q for kw in tech_kw):
        return "D"

    # 전략
    strat_kw = ["전략", "strategy", "진입", "포지셔닝", "의사결정", "시나리오"]
    if any(kw in q for kw in strat_kw):
        return "C"

    # 시장/경쟁 (기본)
    return "A"


def inject_context(query: str, domain: str) -> str:
    """STAGE 3: 컨텍스트 인젝션 (헤더 삽입)"""
    today = datetime.now().strftime("%Y-%m-%d")
    quarter = f"Q{(datetime.now().month - 1) // 3 + 1} {datetime.now().year}"
    header = f"[CONTEXT: domain={domain} | date={today} | quarter={quarter}]\n"
    return header + query


def determine_format_spec(intent_class: str, query: str) -> dict:
    """STAGE 4: 출력 포맷 결정"""
    depth_map = {"A": 3, "B": 4, "C": 3, "D": 4, "E": "L3_delegate"}
    table_required_classes = {"B", "D"}

    return {
        "depth": depth_map.get(intent_class, 3),
        "lang": "ko",
        "citation_mode": "inline",
        "table_required": intent_class in table_required_classes or len(query) > 200,
    }


def check_layer3_escalation(query: str, domain: str, intent_class: str) -> tuple[bool, list]:
    """Layer 3 에스컬레이션 여부 + 실행 모듈 결정"""
    # [DEEP] 명시 플래그
    if "[DEEP]" in query:
        modules = list(LAYER3_KEYWORDS.get(domain, {}).keys()) if domain in LAYER3_DOMAINS else []
        return True, modules

    # CLASS-E 자동 에스컬레이션
    if intent_class == "E" and domain in LAYER3_DOMAINS:
        return True, [f"{domain}-ALL"]

    # 도메인별 키워드 트리거
    if domain in LAYER3_DOMAINS:
        keywords = LAYER3_KEYWORDS.get(domain, [])
        triggered = [kw for kw in keywords if kw.lower() in query.lower()]
        if triggered:
            module_map = {
                "PE-AI-ECO": ["A-1", "A-2", "A-3"],
                "PE-SEMI": ["B-1", "B-2", "B-3"],
                "PE-DD": ["C-1", "C-2", "C-3", "C-4"],
            }
            return True, module_map.get(domain, [])

    return False, []


def preprocess_gate(
    query: str,
    domain: str,
    verbose: bool = False
) -> RoutingPacket:
    """
    PE-VC-02 전처리 게이트 메인 함수
    Returns: RoutingPacket
    """
    # STAGE 1
    norm_query = normalize_query(query)

    # STAGE 2
    intent_class = classify_intent(norm_query, domain)

    # STAGE 3
    enriched_query = inject_context(norm_query, domain)

    # STAGE 4
    fmt_spec = determine_format_spec(intent_class, norm_query)

    # Layer 3 에스컬레이션 판단
    l3_escalate, l3_modules = check_layer3_escalation(norm_query, domain, intent_class)

    packet = RoutingPacket(
        normalized_query=enriched_query,
        intent_class=intent_class,
        primary_domain=domain,
        context_injected=True,
        layer3_escalate=l3_escalate,
        layer3_modules=l3_modules,
        format_spec=fmt_spec,
    )

    if verbose:
        print(packet.to_yaml_str())

    return packet


# ──────────────────────────────────────────────
# Layer 3 — 심층 분석 디스패처
# ──────────────────────────────────────────────

def layer3_dispatch(packet: RoutingPacket) -> dict:
    """
    PE-VC-03 심층 분석 디스패치
    실제 AI 호출은 외부 오케스트레이터에 위임; 이 함수는 실행 명세 반환
    """
    if not packet.layer3_escalate:
        return {"status": "SKIP", "reason": "layer3_escalate=false"}

    domain = packet.primary_domain
    if domain not in LAYER3_DOMAINS:
        return {"status": "SKIP", "reason": f"{domain} not in LAYER3_DOMAINS"}

    module_specs = {
        "PE-AI-ECO": {
            "A-1": "생태계 구조 매핑",
            "A-2": "기술 가속도 분석",
            "A-3": "투자 시그널 추출",
        },
        "PE-SEMI": {
            "B-1": "GraphSAGE-3L 노드 상태 갱신",
            "B-2": "충격 시뮬레이션 3시나리오",
            "B-3": "선단 공정 로드맵 갱신",
        },
        "PE-DD": {
            "C-1": "재무 건전성 다층 진단",
            "C-2": "밸류에이션 크로스체크",
            "C-3": "거버넌스 리스크",
            "C-4": "출구 전략 매핑",
        },
    }

    modules_to_run = [
        {"id": m, "description": module_specs[domain].get(m, m)}
        for m in packet.layer3_modules
    ]

    return {
        "status": "EXECUTE",
        "domain": domain,
        "modules": modules_to_run,
        "query": packet.normalized_query,
        "format_spec": packet.format_spec,
        "timestamp": packet.timestamp,
    }


# ──────────────────────────────────────────────
# CLI 인터페이스
# ──────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python vc_layer_router.py <query> <domain> [--verbose]")
        print("Example: python vc_layer_router.py 'TSMC CoWoS 공급망 충격 시뮬레이션' PE-SEMI --verbose")
        sys.exit(0)

    raw_query = sys.argv[1]
    target_domain = sys.argv[2]
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    packet = preprocess_gate(raw_query, target_domain, verbose=verbose)

    print("\n=== PE-VC-02 Layer 2 라우팅 패킷 ===")
    print(packet.to_yaml_str())

    if packet.layer3_escalate:
        print("\n=== PE-VC-03 Layer 3 심층 분석 명세 ===")
        l3_result = layer3_dispatch(packet)
        print(json.dumps(l3_result, ensure_ascii=False, indent=2))
    else:
        print("\n→ Layer 3 에스컬레이션 없음: 도메인 프롬프트 직접 실행")
