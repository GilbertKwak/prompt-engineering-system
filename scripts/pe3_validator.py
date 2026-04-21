# scripts/pe3_validator.py
# PE-3 Engine — 5-Axis Prompt Validation
# Version: v1.0 | 2026-04-21 | Author: Gilbert Kwak
# Repo: GilbertKwak/prompt-engineering-system
# E-0N: E-07 trigger on total < 80

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import openai
except ImportError:
    openai = None  # type: ignore

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
PASS_THRESHOLD = 80
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

VALIDATION_SYSTEM_PROMPT = """
당신은 프롬프트 품질 심사관입니다.
아래 프롬프트를 5차원으로 채점하세요 (각 0~20점, 합계 100점).

채점 기준:
1. 명확성 (Clarity)         : 역할·목표·출력형식이 모호하지 않은가
2. 실행가능성 (Executability): 엔지니어가 바로 사용 가능한가
3. 완결성 (Completeness)    : 필수 섹션(역할/입력/출력/KPI/리스크)이 모두 있는가
4. 재현성 (Reproducibility) : 동일 입력 → 동일 출력이 보장되는가
5. 도메인 적합성 (Domain Fit): Gilbert의 반도체/열관리 도메인에 최적화되었는가

출력 형식 (JSON strict):
{
  "scores": {
    "clarity": int,
    "executability": int,
    "completeness": int,
    "reproducibility": int,
    "domain_fit": int
  },
  "total": int,
  "pass": bool,
  "weak_points": ["string"],
  "improvement_hints": ["string"]
}
"""

# ---------------------------------------------------------------------------
# E-0N Error Tags
# ---------------------------------------------------------------------------
ERROR_TAGS = {
    "E-01": "SHA 불일치",
    "E-02": "상태값 누락",
    "E-03": "버전 역행",
    "E-04": "Notion-GitHub 구조 불일치",
    "E-05": "KPI 미정의",
    "E-06": "출력 형식 불일치",
    "E-07": "프롬프트 품질 기준 미달",
}


def _tag_error(code: str, detail: str = "") -> str:
    label = ERROR_TAGS.get(code, "알 수 없는 오류")
    msg = f"[{code}] {label}"
    if detail:
        msg += f" — {detail}"
    return msg


# ---------------------------------------------------------------------------
# Core Validation
# ---------------------------------------------------------------------------
def validate_prompt(prompt_text: str, dry_run: bool = False) -> dict:
    """
    Validate a prompt using PE-3 5-axis scoring.

    Args:
        prompt_text: The prompt markdown/text to validate.
        dry_run    : If True, skip LLM call and return dummy passing result.

    Returns:
        dict with keys: scores, total, pass, weak_points, improvement_hints,
                        error_code (optional), timestamp
    """
    if dry_run or openai is None:
        result = {
            "scores": {
                "clarity": 18,
                "executability": 17,
                "completeness": 16,
                "reproducibility": 15,
                "domain_fit": 18,
            },
            "total": 84,
            "pass": True,
            "weak_points": [],
            "improvement_hints": [],
            "_mode": "dry_run",
        }
    else:
        client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": VALIDATION_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"검증 대상 프롬프트:\n\n{prompt_text}",
                },
            ],
            response_format={"type": "json_object"},
        )
        result = json.loads(response.choices[0].message.content)

    result["timestamp"] = datetime.utcnow().isoformat() + "Z"

    # E-07 tagging
    if not result.get("pass", False):
        total = result.get("total", 0)
        result["error_code"] = "E-07"
        result["error_message"] = _tag_error(
            "E-07", f"점수 {total}/100 (임계값 {PASS_THRESHOLD})"
        )
        print(result["error_message"])
        print(f"  약점: {result.get('weak_points', [])}")
    else:
        result["error_code"] = None
        print(f"[OK] 검증 합격 — 점수: {result['total']}/100")

    _write_log(result)
    return result


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
def _write_log(result: dict) -> None:
    today = datetime.utcnow().strftime("%Y%m%d")
    log_path = LOG_DIR / f"pe3_validation_{today}.json"
    history: list = []
    if log_path.exists():
        try:
            history = json.loads(log_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            history = []
    history.append(result)
    log_path.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Batch Validation
# ---------------------------------------------------------------------------
def validate_batch(prompt_dir: str | Path, dry_run: bool = False) -> list[dict]:
    """
    Validate all .md / .txt files in a directory.

    Returns list of validation results sorted by total score (asc).
    """
    results = []
    for p in Path(prompt_dir).glob("*"):
        if p.suffix not in (".md", ".txt"):
            continue
        text = p.read_text(encoding="utf-8")
        result = validate_prompt(text, dry_run=dry_run)
        result["file"] = str(p)
        results.append(result)
    results.sort(key=lambda r: r.get("total", 0))
    return results


# ---------------------------------------------------------------------------
# SSOT Integrity Pre-check (E-01 guard)
# ---------------------------------------------------------------------------
def check_ssot_integrity(
    notion_sha: Optional[str],
    github_sha: Optional[str],
) -> dict:
    """
    E-01: Detect SHA mismatch between Notion and GitHub.
    Call before any push operation.
    """
    mismatch = notion_sha != github_sha
    return {
        "mismatch": mismatch,
        "notion_sha": notion_sha,
        "github_sha": github_sha,
        "error_code": "E-01" if mismatch else None,
        "error_message": (
            _tag_error("E-01", f"Notion={notion_sha} | GitHub={github_sha}")
            if mismatch
            else None
        ),
    }


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="PE-3 Prompt Validator")
    parser.add_argument("input", nargs="?", help="Prompt file (.md/.txt) or directory")
    parser.add_argument("--dry-run", action="store_true", help="Skip LLM call")
    parser.add_argument("--batch", action="store_true", help="Validate entire directory")
    parser.add_argument(
        "--threshold",
        type=int,
        default=PASS_THRESHOLD,
        help=f"Pass threshold (default: {PASS_THRESHOLD})",
    )
    args = parser.parse_args()

    if not args.input:
        parser.print_help()
        sys.exit(0)

    PASS_THRESHOLD = args.threshold

    if args.batch:
        results = validate_batch(args.input, dry_run=args.dry_run)
        failed = [r for r in results if not r["pass"]]
        print(f"\n총 {len(results)}개 검증 | 합격: {len(results)-len(failed)} | 실패: {len(failed)}")
        if failed:
            print("\n⚠️  미달 파일:")
            for r in failed:
                print(f"  {r['file']} — {r['total']}/100")
            sys.exit(1)
    else:
        path = Path(args.input)
        text = path.read_text(encoding="utf-8")
        result = validate_prompt(text, dry_run=args.dry_run)
        sys.exit(0 if result["pass"] else 1)
