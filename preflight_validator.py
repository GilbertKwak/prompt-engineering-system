#!/usr/bin/env python3
"""
preflight_validator.py
======================
Validates tool_registry.yaml for:
  1. Schema integrity (required fields per tool)
  2. meta.total_tools == actual tool count
  3. Duplicate tool IDs
  4. Version format (semver)
  5. Category whitelist
  6. last_validated is recent (warn if > 30 days)

Outputs:
  - Console summary
  - preflight_report.json
  - GitHub Actions outputs (if --output-github-actions)
"""

import sys
import os
import json
import re
import argparse
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml")
    sys.exit(1)

# ── Constants ────────────────────────────────────────────────
REGISTRY_PATH = os.environ.get("REGISTRY_PATH", "tool_registry.yaml")
REPORT_PATH   = "preflight_report.json"

REQUIRED_META_KEYS = {"version", "total_tools", "last_validated", "maintainer"}
REQUIRED_TOOL_KEYS = {"id", "name", "category", "version", "status", "description"}

ALLOWED_CATEGORIES = {
    "prompt_engineering", "investment", "intelligence",
    "automation", "data_processing", "knowledge_graph",
    "validation", "reporting", "integration", "utility"
}

ALLOWED_STATUSES = {"active", "beta", "deprecated", "experimental", "archived"}

SEMVER_RE = re.compile(r'^\d+\.\d+(\.\d+)?$')


# ── Helpers ──────────────────────────────────────────────────
def github_output(key: str, value: str):
    """Write to GITHUB_OUTPUT if running in CI."""
    gho = os.environ.get("GITHUB_OUTPUT")
    if gho:
        with open(gho, "a") as f:
            f.write(f"{key}={value}\n")


def load_registry(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ── Validators ───────────────────────────────────────────────
def check_meta(meta: dict, errors: list, warnings: list):
    missing = REQUIRED_META_KEYS - set(meta.keys())
    for k in missing:
        errors.append(f"meta: missing required key '{k}'")

    if "last_validated" in meta:
        try:
            lv = datetime.fromisoformat(str(meta["last_validated"]))
            if lv.tzinfo is None:
                lv = lv.replace(tzinfo=timezone.utc)
            age_days = (datetime.now(timezone.utc) - lv).days
            if age_days > 30:
                warnings.append(f"meta.last_validated is {age_days} days old — consider updating")
        except (ValueError, TypeError):
            errors.append("meta.last_validated is not a valid ISO date")

    if "version" in meta and not SEMVER_RE.match(str(meta["version"])):
        errors.append(f"meta.version '{meta['version']}' is not valid semver (e.g. 1.0.0)")


def check_tools(tools: list, errors: list, warnings: list) -> int:
    seen_ids = {}
    valid_count = 0

    for i, tool in enumerate(tools):
        tid = tool.get("id", f"<index {i}>")
        tool_errors = []

        # Required fields
        missing = REQUIRED_TOOL_KEYS - set(tool.keys())
        for k in missing:
            tool_errors.append(f"  [{tid}] missing required field '{k}'")

        # Duplicate ID
        if "id" in tool:
            if tool["id"] in seen_ids:
                tool_errors.append(f"  [{tid}] duplicate ID (first seen at index {seen_ids[tool['id']]})")
            else:
                seen_ids[tool["id"]] = i

        # Category
        if "category" in tool and tool["category"] not in ALLOWED_CATEGORIES:
            tool_errors.append(
                f"  [{tid}] unknown category '{tool['category']}'. "
                f"Allowed: {sorted(ALLOWED_CATEGORIES)}"
            )

        # Status
        if "status" in tool and tool["status"] not in ALLOWED_STATUSES:
            tool_errors.append(
                f"  [{tid}] unknown status '{tool['status']}'. "
                f"Allowed: {sorted(ALLOWED_STATUSES)}"
            )

        # Version format
        if "version" in tool and not SEMVER_RE.match(str(tool["version"])):
            warnings.append(f"  [{tid}] version '{tool['version']}' is not semver")

        # Description length
        if "description" in tool and len(tool["description"]) < 10:
            warnings.append(f"  [{tid}] description is very short")

        if tool_errors:
            errors.extend(tool_errors)
        else:
            valid_count += 1

    return valid_count


def check_count(meta: dict, actual: int, errors: list):
    declared = meta.get("total_tools")
    if declared is None:
        return
    if int(declared) != actual:
        errors.append(
            f"meta.total_tools={declared} but actual tool count={actual}. "
            f"Update meta.total_tools after adding/removing tools."
        )


# ── Main ─────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Validate tool_registry.yaml")
    parser.add_argument("--output-github-actions", action="store_true")
    parser.add_argument("--registry", default=REGISTRY_PATH)
    args = parser.parse_args()

    registry_path = args.registry

    print(f"\n{'='*60}")
    print("  🛡️  PREFLIGHT VALIDATOR")
    print(f"  Registry: {registry_path}")
    print(f"  Time: {datetime.now(timezone.utc).isoformat()}")
    print(f"{'='*60}\n")

    if not Path(registry_path).exists():
        print(f"❌ FATAL: {registry_path} not found")
        sys.exit(1)

    try:
        data = load_registry(registry_path)
    except yaml.YAMLError as e:
        print(f"❌ FATAL: YAML parse error:\n{e}")
        sys.exit(1)

    errors   = []
    warnings = []

    meta  = data.get("meta", {})
    tools = data.get("tools", [])

    if not isinstance(meta, dict):
        errors.append("'meta' section is missing or not a mapping")
        meta = {}

    if not isinstance(tools, list):
        errors.append("'tools' section is missing or not a list")
        tools = []

    check_meta(meta, errors, warnings)
    valid_count = check_tools(tools, errors, warnings)
    check_count(meta, len(tools), errors)

    # ── Results ──
    status = "PASS" if not errors else "FAIL"
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    report = {
        "status": status,
        "timestamp": now_iso,
        "registry": registry_path,
        "meta": meta,
        "actual_count": len(tools),
        "valid_tools": valid_count,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
    }

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False, default=str)

    # Console output
    if warnings:
        print("⚠️  WARNINGS:")
        for w in warnings:
            print(f"   {w}")
        print()

    if errors:
        print("❌ ERRORS:")
        for e in errors:
            print(f"   {e}")
        print()

    print(f"{'─'*60}")
    print(f"  Status      : {'✅ PASS' if status == 'PASS' else '❌ FAIL'}")
    print(f"  Total tools : {len(tools)} (declared: {meta.get('total_tools', '?')})")
    print(f"  Valid tools : {valid_count}")
    print(f"  Errors      : {len(errors)}")
    print(f"  Warnings    : {len(warnings)}")
    print(f"  Report      : {REPORT_PATH}")
    print(f"{'='*60}\n")

    if args.output_github_actions:
        github_output("status",        status)
        github_output("total_tools",   str(len(tools)))
        github_output("valid_tools",   str(valid_count))
        github_output("error_count",   str(len(errors)))
        github_output("last_validated", now_iso)

    sys.exit(0 if status == "PASS" else 1)


if __name__ == "__main__":
    main()
