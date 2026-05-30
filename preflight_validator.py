#!/usr/bin/env python3
"""
preflight_validator.py
======================
Validates tool_registry.yaml on every push.
Runs as part of .github/workflows/preflight.yml.

Checks:
  1. YAML syntax is valid
  2. meta.total_tools matches the actual count of entries
  3. meta.last_validated is present and a valid ISO date
  4. Every tool entry has required fields
  5. Tool IDs are unique
  6. Tool paths exist in the repository
  7. Category values are within the allowed set
  8. Status values are within the allowed set

Exit codes:
  0  – all checks passed
  1  – validation failed (details printed to stdout)
"""

import sys
import os
import yaml
from datetime import datetime
from pathlib import Path

# ── Configuration ────────────────────────────────────────────
REGISTRY_FILE = "tool_registry.yaml"
ALLOWED_CATEGORIES = {"PE", "FIN", "CON", "AGENT", "INFRA", "DATA"}
ALLOWED_STATUSES = {"active", "beta", "deprecated"}
REQUIRED_TOOL_FIELDS = {"id", "name", "category", "status", "path", "description", "added"}

# ── Colour helpers (ANSI — works in GitHub Actions logs) ─────
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
RESET  = "\033[0m"
BOLD   = "\033[1m"


def ok(msg: str) -> None:
    print(f"{GREEN}  ✓ {msg}{RESET}")


def warn(msg: str) -> None:
    print(f"{YELLOW}  ⚠ {msg}{RESET}")


def fail(msg: str) -> None:
    print(f"{RED}  ✗ {msg}{RESET}")


def header(msg: str) -> None:
    print(f"\n{BOLD}{msg}{RESET}")


def validate_registry(repo_root: Path) -> bool:
    registry_path = repo_root / REGISTRY_FILE
    errors: list[str] = []
    warnings: list[str] = []

    # ── 1. File exists ────────────────────────────────────────
    header("[1] Checking registry file exists")
    if not registry_path.exists():
        fail(f"{REGISTRY_FILE} not found at {registry_path}")
        return False
    ok(f"{REGISTRY_FILE} found")

    # ── 2. YAML syntax ───────────────────────────────────────
    header("[2] Parsing YAML")
    try:
        with open(registry_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        ok("YAML syntax is valid")
    except yaml.YAMLError as exc:
        fail(f"YAML parse error: {exc}")
        return False

    if not isinstance(data, dict):
        fail("Root document must be a YAML mapping")
        return False

    # ── 3. Meta section ──────────────────────────────────────
    header("[3] Validating meta section")
    meta = data.get("meta", {})

    # last_validated
    last_validated_raw = meta.get("last_validated")
    if last_validated_raw is None:
        errors.append("meta.last_validated is missing")
        fail("meta.last_validated is missing")
    else:
        try:
            datetime.strptime(str(last_validated_raw), "%Y-%m-%d")
            ok(f"meta.last_validated = {last_validated_raw}")
        except ValueError:
            errors.append(f"meta.last_validated '{last_validated_raw}' is not YYYY-MM-DD")
            fail(f"meta.last_validated '{last_validated_raw}' is not YYYY-MM-DD")

    # ── 4. Tools list ────────────────────────────────────────
    header("[4] Validating tools list")
    tools = data.get("tools", [])
    if not isinstance(tools, list):
        fail("'tools' must be a list")
        return False
    ok(f"Found {len(tools)} tool entries in registry")

    # ── 5. total_tools count ─────────────────────────────────
    header("[5] Checking meta.total_tools count")
    declared_count = meta.get("total_tools")
    actual_count = len(tools)
    if declared_count != actual_count:
        msg = (
            f"meta.total_tools={declared_count} but actual count={actual_count}. "
            "Update meta.total_tools in tool_registry.yaml."
        )
        errors.append(msg)
        fail(msg)
    else:
        ok(f"meta.total_tools={declared_count} matches actual count")

    # ── 6. Per-tool validation ───────────────────────────────
    header("[6] Validating individual tool entries")
    seen_ids: set[str] = set()

    for i, tool in enumerate(tools):
        tool_id = tool.get("id", f"<unknown #{i}>")
        prefix = f"  [{tool_id}]"

        # Required fields
        missing = REQUIRED_TOOL_FIELDS - set(tool.keys())
        if missing:
            msg = f"{prefix} missing required fields: {sorted(missing)}"
            errors.append(msg)
            fail(msg)

        # Unique IDs
        if tool_id in seen_ids:
            msg = f"{prefix} duplicate tool ID '{tool_id}'"
            errors.append(msg)
            fail(msg)
        else:
            seen_ids.add(tool_id)

        # Category check
        category = tool.get("category", "")
        if category not in ALLOWED_CATEGORIES:
            msg = f"{prefix} invalid category '{category}' (allowed: {ALLOWED_CATEGORIES})"
            errors.append(msg)
            fail(msg)

        # Status check
        status = tool.get("status", "")
        if status not in ALLOWED_STATUSES:
            msg = f"{prefix} invalid status '{status}' (allowed: {ALLOWED_STATUSES})"
            errors.append(msg)
            fail(msg)

        # Path exists (warn, not error — CI may not have full FS)
        tool_path = tool.get("path", "")
        full_path = repo_root / tool_path
        if not full_path.exists():
            warn(f"{prefix} path does not exist: {tool_path}")
            warnings.append(f"{tool_id}: path not found ({tool_path})")
        else:
            ok(f"{prefix} path OK → {tool_path}")

        # Added date format
        added_raw = tool.get("added", "")
        try:
            datetime.strptime(str(added_raw), "%Y-%m-%d")
        except ValueError:
            msg = f"{prefix} 'added' date '{added_raw}' is not YYYY-MM-DD"
            errors.append(msg)
            fail(msg)

    # ── Summary ──────────────────────────────────────────────
    print("")
    print("═" * 60)
    if errors:
        print(f"{RED}{BOLD}PREFLIGHT FAILED — {len(errors)} error(s){RESET}")
        for e in errors:
            print(f"  • {e}")
        if warnings:
            print(f"\n{YELLOW}Warnings ({len(warnings)}):{RESET}")
            for w in warnings:
                print(f"  • {w}")
        return False
    else:
        print(f"{GREEN}{BOLD}PREFLIGHT PASSED ✓{RESET}")
        print(f"  Tools validated : {actual_count}")
        print(f"  Last validated  : {last_validated_raw}")
        if warnings:
            print(f"\n{YELLOW}Warnings ({len(warnings)}):{RESET}")
            for w in warnings:
                print(f"  • {w}")
        return True


if __name__ == "__main__":
    repo_root = Path(os.environ.get("GITHUB_WORKSPACE", "."))
    print(f"{BOLD}Preflight Validator — tool_registry.yaml{RESET}")
    print(f"Repo root : {repo_root}")
    print(f"Registry  : {repo_root / REGISTRY_FILE}")
    passed = validate_registry(repo_root)
    sys.exit(0 if passed else 1)
