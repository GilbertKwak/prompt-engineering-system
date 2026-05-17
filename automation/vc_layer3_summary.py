#!/usr/bin/env python3
"""PE-VC-03 Layer 3 result summary writer.

Usage:
    python3 automation/vc_layer3_summary.py l3_result.json
Output is written to stdout (redirect >> $GITHUB_STEP_SUMMARY in CI).
"""
import json
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: vc_layer3_summary.py <l3_result.json>", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    try:
        with open(path) as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

    domain = data.get("domain", "N/A")
    status = data.get("status", "N/A")
    timestamp = data.get("timestamp", "")
    modules = data.get("modules", [])
    force = data.get("force_layer3", False)

    lines = ["## \U0001f534 PE-VC-03 Layer 3 \uc2ec\uce35 \ubd84\uc11d \uba85\uc138\n"]
    lines.append(f"**\ub3c4\uba54\uc778**: `{domain}`  ")
    lines.append(f"**\uc0c1\ud0dc**: `{status}`  ")
    lines.append(f"**force\_layer3**: `{force}`  ")
    lines.append(f"**\ud0c0\uc784\uc2a4\ud0ec\ud504**: {timestamp}\n")
    lines.append("### \uc2e4\ud589 \ubaa8\ub4c8")
    lines.append("| \ubaa8\ub4c8 ID | \uc124\uba85 |")
    lines.append("|---------|------|")
    for m in modules:
        lines.append(f"| `{m['id']}` | {m['description']} |")

    summary = "\n".join(lines) + "\n"
    print(summary)


if __name__ == "__main__":
    main()
