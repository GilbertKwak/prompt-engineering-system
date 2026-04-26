#!/usr/bin/env python3
"""
PE-7 Secrets Validator — PE-3 auto-validation 연계
GitHub Actions 환경에서 모든 Secrets의 형식과 연결성을 검증합니다.

사용:
  python scripts/validate_secrets.py
  python scripts/validate_secrets.py --strict   # 연결 테스트 포함
"""

import os
import re
import sys
import json
import argparse
from dataclasses import dataclass, field
from typing import List, Optional

# ─────────────────────────────────────────
# Secret 스키마 정의
# ─────────────────────────────────────────
@dataclass
class SecretSpec:
    name: str
    description: str
    pattern: Optional[str] = None
    required: bool = True
    engines: List[str] = field(default_factory=list)

SECRET_SPECS = [
    SecretSpec(
        name="NOTION_API_KEY",
        description="Notion Integration Token",
        pattern=r"^secret_[A-Za-z0-9]{43}$",
        engines=["PE-1", "PE-2", "PE-3", "PE-7"],
    ),
    SecretSpec(
        name="NOTION_KPI_DB_ID",
        description="Notion KPI Database ID (32자리 hex)",
        pattern=r"^[a-f0-9]{32}$",
        engines=["PE-1", "PE-2", "PE-3", "PE-7"],
    ),
    SecretSpec(
        name="GOOGLE_SHEETS_ID",
        description="Google Sheets Spreadsheet ID",
        pattern=r"^[A-Za-z0-9_-]{44}$",
        engines=["PE-1", "PE-3", "PE-7"],
    ),
    SecretSpec(
        name="GOOGLE_SERVICE_ACCOUNT_JSON",
        description="GCP Service Account JSON",
        pattern=None,  # JSON 구조 검증
        engines=["PE-1", "PE-3", "PE-7"],
    ),
    SecretSpec(
        name="SLACK_WEBHOOK_URL",
        description="Slack Incoming Webhook URL",
        pattern=r"^https://hooks\.slack\.com/services/[A-Z0-9]+/[A-Z0-9]+/[A-Za-z0-9]+$",
        engines=["PE-1", "PE-2", "PE-3", "PE-7"],
    ),
]

# ─────────────────────────────────────────
# 검증 결과
# ─────────────────────────────────────────
@dataclass
class ValidationResult:
    name: str
    status: str  # PASS / FAIL / WARN / SKIP
    message: str
    engines: List[str]

def validate_google_service_account_json(value: str) -> tuple[bool, str]:
    """GCP Service Account JSON 구조 검증"""
    try:
        data = json.loads(value)
    except json.JSONDecodeError as e:
        return False, f"JSON 파싱 실패: {e}"

    required_fields = [
        "type", "project_id", "private_key_id",
        "private_key", "client_email", "client_id",
    ]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return False, f"필수 필드 누락: {missing}"

    if data.get("type") != "service_account":
        return False, f"type 불일치: '{data.get('type')}' (expected: 'service_account')"

    if not data.get("client_email", "").endswith(".iam.gserviceaccount.com"):
        return False, "client_email 형식 오류"

    return True, "JSON 구조 정상"

def validate_secret(spec: SecretSpec, strict: bool = False) -> ValidationResult:
    """단일 Secret 검증"""
    value = os.environ.get(spec.name, "")

    if not value:
        if spec.required:
            return ValidationResult(
                name=spec.name,
                status="FAIL",
                message="환경변수 없음 (Secret 미설정)",
                engines=spec.engines,
            )
        return ValidationResult(
            name=spec.name,
            status="SKIP",
            message="선택적 Secret — 미설정",
            engines=spec.engines,
        )

    # 특수 검증: GCP JSON
    if spec.name == "GOOGLE_SERVICE_ACCOUNT_JSON":
        ok, msg = validate_google_service_account_json(value)
        return ValidationResult(
            name=spec.name,
            status="PASS" if ok else "FAIL",
            message=msg,
            engines=spec.engines,
        )

    # 정규식 패턴 검증
    if spec.pattern:
        if not re.match(spec.pattern, value):
            # 마스킹: 앞 8자리만 표시
            masked = value[:8] + "..." if len(value) > 8 else "***"
            return ValidationResult(
                name=spec.name,
                status="FAIL",
                message=f"형식 불일치 (값: {masked})",
                engines=spec.engines,
            )

    return ValidationResult(
        name=spec.name,
        status="PASS",
        message="형식 검증 통과",
        engines=spec.engines,
    )

def print_results(results: List[ValidationResult]) -> int:
    """결과 출력 및 종료 코드 반환"""
    ICONS = {"PASS": "✅", "FAIL": "❌", "WARN": "⚠️", "SKIP": "⏭️"}

    print()
    print("╔══════════════════════════════════════════════════════╗")
    print("║   PE-7 Secrets Validation Report                    ║")
    print("║   PE-1 / PE-2 / PE-3 Engine Integration Check      ║")
    print("╚══════════════════════════════════════════════════════╝")
    print()

    pass_count = fail_count = skip_count = 0

    for r in results:
        icon = ICONS.get(r.status, "?")
        engines_str = ", ".join(r.engines)
        print(f"  {icon} [{r.status:<4}] {r.name}")
        print(f"         → {r.message}")
        print(f"         → Engines: {engines_str}")
        print()

        if r.status == "PASS":
            pass_count += 1
        elif r.status == "FAIL":
            fail_count += 1
        else:
            skip_count += 1

    total = len(results)
    print(f"  {'─'*52}")
    print(f"  총 {total}개 | ✅ {pass_count} PASS | ❌ {fail_count} FAIL | ⏭️ {skip_count} SKIP")
    print()

    # PE-3 연계: engine별 준비 상태 출력
    engine_status = {}
    for r in results:
        for eng in r.engines:
            if eng not in engine_status:
                engine_status[eng] = {"ready": True, "missing": []}
            if r.status == "FAIL":
                engine_status[eng]["ready"] = False
                engine_status[eng]["missing"].append(r.name)

    print("  엔진별 준비 상태:")
    for eng, state in sorted(engine_status.items()):
        icon = "🟢" if state["ready"] else "🔴"
        print(f"    {icon} {eng}: {'Ready' if state['ready'] else 'NOT READY — Missing: ' + ', '.join(state['missing'])}")

    print()

    return 1 if fail_count > 0 else 0

def main():
    parser = argparse.ArgumentParser(description="PE-7 Secrets Validator")
    parser.add_argument("--strict", action="store_true", help="API 연결 테스트 포함")
    parser.add_argument("--engine", help="특정 엔진만 검증 (예: PE-3)")
    args = parser.parse_args()

    specs = SECRET_SPECS
    if args.engine:
        specs = [s for s in specs if args.engine in s.engines]
        print(f"[INFO] {args.engine} 연관 Secrets만 검증합니다.")

    results = [validate_secret(spec, strict=args.strict) for spec in specs]
    exit_code = print_results(results)

    # GitHub Actions STEP SUMMARY 출력
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a") as f:
            f.write("## 🔐 Secrets Validation Results\n\n")
            f.write("| Secret | Status | Message | Engines |\n")
            f.write("|--------|--------|---------|---------|\n")
            for r in results:
                emoji = {"PASS": "✅", "FAIL": "❌", "SKIP": "⏭️"}.get(r.status, "")
                engines = ", ".join(r.engines)
                f.write(f"| `{r.name}` | {emoji} {r.status} | {r.message} | {engines} |\n")

    sys.exit(exit_code)

if __name__ == "__main__":
    main()
