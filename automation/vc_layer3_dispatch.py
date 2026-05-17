#!/usr/bin/env python3
"""PE-VC-03 Layer 3 deep-analysis dispatcher.

Usage:
    python3 automation/vc_layer3_dispatch.py \
        --query <query> --domain <domain> --force <true|false> --output l3_result.json
"""
import argparse
import json
import sys
from datetime import datetime, timezone

LAYER3_MODULE_MAP = {
    "PE-AI-ECO": [
        {"id": "L3-AI-01", "description": "AI \uc5d0\ucf54\uc2dc\uc2a4\ud15c \uacbd\uc7c1 \uc9c0\ub3c4 \uc2ec\uce35 \ub9e4\ud551"},
        {"id": "L3-AI-02", "description": "LLM \uc778\ud504\ub77c \uac00\uce58\uc0ac\uc2ac \uc548\uc815\uc131 \uc2a4\ucf54\uc5b4\ub9c1"},
        {"id": "L3-AI-03", "description": "\uc804\ub825/\ub370\uc774\ud130\uc13c\ud130 \uc758\uc874\ub3c4 GNN \ubd84\uc11d"},
    ],
    "PE-SEMI": [
        {"id": "L3-SEMI-01", "description": "\uc804\uacf5\uc815 \ubcd1\ubaa9 \ub178\ub4dc GraphSAGE \uc2e0\ud638"},
        {"id": "L3-SEMI-02", "description": "HBM/CoWoS \uc218\uae09 \uc5fc\ub824 \uc218\uc900 \uc815\ub7c9 \ud655\uc778"},
        {"id": "L3-SEMI-03", "description": "\ubbf8\uc911 \uc7a5\ube44 \uade0\ud615 \ucc28\uc775 \ucda9\uaca9 \uc2dc\ubbac"},
    ],
    "PE-DD": [
        {"id": "L3-DD-01", "description": "DD \uc704\ud5d8 \ucda9 \ubca4\uce58\ub9c8\ud0a4 \ud321 \uc2e4\uc0ac"},
        {"id": "L3-DD-02", "description": "\uc7ac\ubb34 \ubaa8\ub378 DCF/\uba40\ud2f0\ud50c \uac00\uc2dc\ud654"},
        {"id": "L3-DD-03", "description": "\ubc95\ubb34/\uaddc\uc81c \ub9ac\uc2a4\ud06c \ud50c\ub798\uadf8 \ud0d0\uc9c0"},
    ],
}


def dispatch(query: str, domain: str, force: bool) -> dict:
    modules = LAYER3_MODULE_MAP.get(domain, [])
    if not modules:
        print(f"[WARN] No Layer 3 modules registered for domain: {domain}", file=sys.stderr)

    if force:
        query = query + " [DEEP]"

    return {
        "domain": domain,
        "query": query,
        "force_layer3": force,
        "status": "dispatched",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "modules": modules,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--domain", required=True)
    parser.add_argument("--force", default="false")
    parser.add_argument("--output", default="l3_result.json")
    args = parser.parse_args()

    force = args.force.lower() in ("true", "1", "yes")
    result = dispatch(args.query, args.domain, force)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    with open(args.output, "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
