#!/usr/bin/env python3
"""PE-VC-03 Layer 3 deep-analysis dispatcher.

P3 업데이트: 하드코딩된 LAYER3_MODULE_MAP 제거,
         vc_layer_router.preprocess_gate + layer3_dispatch 실제 로직으로 교체.
P4 지원: force=true 시 쿼리에 [DEEP] 플래그 주입 → vc_layer_router 내부 키워드에서
          check_layer3_escalation이 자동 모듈 배팅.

Usage:
    python3 automation/vc_layer3_dispatch.py \
        --query <query> --domain <domain> --force <true|false> --output l3_result.json
"""
import argparse
import json
import sys
import os
from datetime import datetime, timezone

# automation/ 파일이 저장소 루트에서 실행될 수 있으므로 sys.path 보저
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from vc_layer_router import preprocess_gate, layer3_dispatch


def run(query: str, domain: str, force: bool) -> dict:
    """P4: force=true 시 [DEEP] 플래그 주입으로 vc_layer_router의
    check_layer3_escalation을 강제 트리거."""
    if force:
        query = query.rstrip() + " [DEEP]"

    packet = preprocess_gate(query, domain, verbose=False)

    # force=true인 경우 layer3_escalate를 강제 True로 덜우르고
    # 해당 도메인 모듈 전체를 modules_to_run에 인가
    if force and not packet.layer3_escalate:
        packet.layer3_escalate = True
        # 도메인 모듈 전체 주입
        full_module_map = {
            "PE-AI-ECO": ["A-1", "A-2", "A-3"],
            "PE-SEMI":   ["B-1", "B-2", "B-3"],
            "PE-DD":     ["C-1", "C-2", "C-3", "C-4"],
        }
        packet.layer3_modules = full_module_map.get(domain, [])

    result = layer3_dispatch(packet)

    # layer3_dispatch가 SKIP을 리턴하는 경우(도메인 불일치 등) 경고 출력
    if result.get("status") == "SKIP":
        print(f"[WARN] Layer 3 SKIP: {result.get('reason')}", file=sys.stderr)

    # 모든 컠담 timestamp 통일
    result["timestamp"] = datetime.now(timezone.utc).isoformat()
    result["force_layer3"] = force
    result["domain"] = domain

    return result


def main():
    parser = argparse.ArgumentParser(description="PE-VC-03 Layer 3 Dispatcher")
    parser.add_argument("--query",  required=True,  help="분석 쿼리")
    parser.add_argument("--domain", required=True,  help="대상 도메인 (PE-SEMI 등)")
    parser.add_argument("--force",  default="false", help="Layer 3 강제 실행 (true/false)")
    parser.add_argument("--output", default="l3_result.json", help="출력 JSON 경로")
    args = parser.parse_args()

    force = args.force.lower() in ("true", "1", "yes")
    result = run(args.query, args.domain, force)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"[OK] Layer 3 result saved to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
