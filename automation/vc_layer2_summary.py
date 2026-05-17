#!/usr/bin/env python3
"""PE-VC-02 Layer 2 preprocessing gate summary writer.

Usage:
    python3 automation/vc_layer2_summary.py routing_packet.txt
Output is written to stdout (redirect >> $GITHUB_STEP_SUMMARY in CI).
"""
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: vc_layer2_summary.py <routing_packet.txt>", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    try:
        content = open(path).read()
    except FileNotFoundError:
        print(f"[ERROR] File not found: {path}", file=sys.stderr)
        sys.exit(1)

    lines = content.strip().split("\n")

    summary = "## \U0001f535 PE-VC-02 Layer 2 \uc804\uccb2\ub9ac \uacb0\uacfc\n\n"
    summary += "| \ud56d\ubaa9 | \uac12 |\n|------|-----|\n"

    for line in lines:
        if ":" in line and not line.startswith("#"):
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            if key and val:
                summary += f"| `{key}` | {val} |\n"

    print(summary)


if __name__ == "__main__":
    main()
