# scripts/pe1_improver.py
# PE-1 Engine — Prompt Auto-Improvement
# Version: v1.0 | 2026-04-21 | Author: Gilbert Kwak
# Repo: GilbertKwak/prompt-engineering-system
# Depends on: pe3_validator.py (for weak_points / improvement_hints)

from __future__ import annotations

import difflib
import json
import os
import re
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Optional

try:
    import openai
except ImportError:
    openai = None  # type: ignore

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

IMPROVEMENT_SYSTEM_PROMPT = """
당신은 프롬프트 개선 전문가입니다.

작업 규칙:
1. 아래 원본 프롬프트의 약점(weak_points)을 분석
2. 개선 힌트(improvement_hints)를 반영하여 섹션 단위로 재작성
3. 원본 구조(섹션 순서·헤더명)는 반드시 유지
4. 코드 스니펫은 보강만 허용 — 삭제 절대 금지
5. 추상적 문장 → 구체적 코드/예시로 교체
6. 누락 섹션 → 템플릿 기반 자동 보충
7. 버전은 자동 +0.1 증분 (예: v2.0 → v2.1)
8. 출력: 완전한 마크다운 프롬프트 전문만 출력 (설명 문장 금지)

절대 금지:
- 원본에 없는 섹션 삭제
- 코드 블록 제거
- 버전 번호 감소
"""


# ---------------------------------------------------------------------------
# Version Auto-Increment
# ---------------------------------------------------------------------------
def _bump_version(text: str) -> tuple[str, str]:
    """
    Find version pattern (vX.Y) in text and increment minor by 0.1.
    Returns (updated_text, new_version_string).
    """
    pattern = re.compile(r'v(\d+)\.(\d+)')
    match = pattern.search(text)
    if not match:
        return text, "v1.0"
    major = int(match.group(1))
    minor = int(match.group(2)) + 1
    new_ver = f"v{major}.{minor}"
    updated = pattern.sub(new_ver, text, count=1)
    return updated, new_ver


# ---------------------------------------------------------------------------
# Diff Logger
# ---------------------------------------------------------------------------
def log_improvement_diff(before: str, after: str, label: str = "") -> Path:
    """
    Write unified diff of before/after to logs/improvement_YYYYMMDD.diff.
    Returns path to written log file.
    """
    diff_lines = list(
        difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile="before",
            tofile="after",
        )
    )
    log_path = LOG_DIR / f"improvement_{date.today().strftime('%Y%m%d')}.diff"
    header = f"# PE-1 Improvement Diff — {datetime.utcnow().isoformat()}Z"
    if label:
        header += f" | {label}"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(header + "\n")
        f.writelines(diff_lines)
        f.write("\n" + "-" * 60 + "\n")
    return log_path


# ---------------------------------------------------------------------------
# Core Improvement
# ---------------------------------------------------------------------------
def improve_prompt(
    original: str,
    weak_points: list[str],
    hints: list[str],
    dry_run: bool = False,
) -> dict:
    """
    Improve a prompt based on PE-3 validator output.

    Args:
        original   : Original prompt text (markdown).
        weak_points: List of identified weaknesses from pe3_validator.
        hints      : List of improvement directions from pe3_validator.
        dry_run    : If True, skip LLM call and return original with bumped version.

    Returns:
        dict with keys: improved_prompt, new_version, change_log, diff_path, timestamp
    """
    if not weak_points and not hints:
        print("[SKIP] weak_points / hints 없음 — 개선 불필요")
        return {
            "improved_prompt": original,
            "new_version": None,
            "change_log": "개선 불필요 (이미 합격)",
            "diff_path": None,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    context = (
        f"원본 프롬프트:\n{original}\n\n"
        f"약점 목록:\n"
        + "\n".join(f"- {w}" for w in weak_points)
        + "\n\n개선 방향:\n"
        + "\n".join(f"- {h}" for h in hints)
    )

    if dry_run or openai is None:
        improved_raw = original  # 구조 유지
        print("[dry_run] LLM 호출 생략 — 원본 반환")
    else:
        client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": IMPROVEMENT_SYSTEM_PROMPT},
                {"role": "user", "content": context},
            ],
        )
        improved_raw = response.choices[0].message.content

    # Version bump
    improved, new_ver = _bump_version(improved_raw)

    # Diff logging
    diff_path = log_improvement_diff(original, improved, label=new_ver)

    change_log = (
        f"PE-1 자동개선 적용 → {new_ver} "
        f"({len(weak_points)}개 약점 수정, {len(hints)}개 힌트 적용)"
    )
    print(f"[OK] {change_log}")
    print(f"  Diff 로그: {diff_path}")

    result = {
        "improved_prompt": improved,
        "new_version": new_ver,
        "change_log": change_log,
        "diff_path": str(diff_path),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    _write_json_log(result)
    return result


# ---------------------------------------------------------------------------
# JSON Log
# ---------------------------------------------------------------------------
def _write_json_log(result: dict) -> None:
    today = datetime.utcnow().strftime("%Y%m%d")
    log_path = LOG_DIR / f"pe1_improvement_{today}.json"
    history: list = []
    if log_path.exists():
        try:
            history = json.loads(log_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            history = []
    # Store summary only (no full prompt text to keep log light)
    summary = {
        k: v for k, v in result.items() if k != "improved_prompt"
    }
    history.append(summary)
    log_path.write_text(
        json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8"
    )


# ---------------------------------------------------------------------------
# Iterative Improvement Loop (max 3 rounds)
# ---------------------------------------------------------------------------
def improve_until_pass(
    original: str,
    validator_fn,  # callable: (str) -> dict  — pe3_validator.validate_prompt
    max_rounds: int = 3,
    dry_run: bool = False,
) -> dict:
    """
    Run improve → validate loop until pass=True or max_rounds reached.

    Args:
        original    : Starting prompt text.
        validator_fn: pe3_validator.validate_prompt (injected to avoid circular import).
        max_rounds  : Maximum improvement iterations.
        dry_run     : Passed through to improve_prompt and validator_fn.

    Returns:
        dict with final prompt, final validation result, rounds taken.
    """
    current = original
    for rnd in range(1, max_rounds + 1):
        print(f"\n--- [Round {rnd}/{max_rounds}] 검증 실행 ---")
        val = validator_fn(current, dry_run=dry_run)
        if val["pass"]:
            print(f"[합격] Round {rnd} 검증 통과 — {val['total']}/100")
            return {
                "final_prompt": current,
                "validation": val,
                "rounds": rnd,
                "status": "pass",
            }
        print(f"[미달] Round {rnd} 점수: {val['total']}/100 — 개선 실행")
        result = improve_prompt(
            current,
            val["weak_points"],
            val["improvement_hints"],
            dry_run=dry_run,
        )
        current = result["improved_prompt"]

    print(f"[E-07] {max_rounds}회 개선 후에도 미달 — 수동 검토 필요")
    return {
        "final_prompt": current,
        "validation": val,
        "rounds": max_rounds,
        "status": "fail",
    }


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="PE-1 Prompt Improver")
    parser.add_argument("input", help="Prompt file (.md/.txt)")
    parser.add_argument("--weak-points", nargs="*", default=[], help="Weak point strings")
    parser.add_argument("--hints", nargs="*", default=[], help="Improvement hint strings")
    parser.add_argument("--dry-run", action="store_true", help="Skip LLM call")
    parser.add_argument("--output", help="Save improved prompt to file")
    args = parser.parse_args()

    path = Path(args.input)
    text = path.read_text(encoding="utf-8")

    result = improve_prompt(
        text,
        weak_points=args.weak_points,
        hints=args.hints,
        dry_run=args.dry_run,
    )

    if args.output:
        out_path = Path(args.output)
        out_path.write_text(result["improved_prompt"], encoding="utf-8")
        print(f"[저장] {out_path}")
    else:
        print("\n--- 개선된 프롬프트 ---")
        print(result["improved_prompt"])
