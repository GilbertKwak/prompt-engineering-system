# scripts/pe2_proliferator.py
# PE-2 Engine — Prompt Auto-Proliferation
# Version: v1.0 | 2026-04-21 | Author: Gilbert Kwak
# Repo: GilbertKwak/prompt-engineering-system
# Depends on: pe1_improver.py (for base improved prompt)

from __future__ import annotations

import itertools
import json
import os
import random
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
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
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
LOG_DIR = Path("logs")
PROMPT_OUT_DIR = Path("prompts/variants")
LOG_DIR.mkdir(exist_ok=True)
PROMPT_OUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Proliferation Matrix
# ---------------------------------------------------------------------------
PROLIFERATION_MATRIX: dict[str, list[str]] = {
    "domains": [
        "HBM 열관리 보고서 자동화",
        "반도체 공급망 모니터링",
        "sCO2 에너지 시스템 분석",
        "GitHub Actions CI/CD 파이프라인",
    ],
    "levels": [
        "입문 (MVP 단일 스크립트)",
        "중급 (스케줄 자동화)",
        "고급 (멀티 레포 + AI 예측)",
    ],
    "formats": [
        "Python 스크립트",
        "GitHub Actions YAML",
        "Notion 자동화 레시피",
    ],
}

PROLIFERATION_SYSTEM_PROMPT = """
당신은 프롬프트 확장 전문가입니다.
원본 프롬프트를 주어진 도메인·난이도·포맷에 맞게 변형하세요.

절대 규칙:
1. 원본의 7단계 구조 유지 (역할/뮪표/입력/출력/KPI/리스크/철학)
2. 도메인 특화 예시 코드 1개 이상 삽입
3. 난이도에 맞는 도구 스택으로 교체
4. 돈뎽립 실행 가능한 완결 프롬프트
5. 제목: [PE-7] {domain} {level}판 v1.0
6. 코드 스니펫 삭제 절대 금지
7. 추상적 문장 금지 — 실제 도구/API/컴맨드 명시
"""


# ---------------------------------------------------------------------------
# Single Variant Generator
# ---------------------------------------------------------------------------
def _generate_single_variant(
    base_prompt: str,
    domain: str,
    level: str,
    fmt: str,
    dry_run: bool = False,
) -> dict:
    """
    Generate one variant for a given (domain, level, format) combination.
    Returns dict with domain, level, format, content, notion_title, timestamp.
    """
    notion_title = f"[PE-7] {domain[:12]} {level[:4]}판 v1.0"

    if dry_run or openai is None:
        content = (
            f"# {notion_title}\n\n"
            f"[dry_run] 도메인: {domain} | 난이도: {level} | 포맷: {fmt}\n\n"
            + base_prompt[:500]
            + "\n..."
        )
    else:
        client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        user_msg = (
            f"원본 프롬프트 (앞 2000자):\n{base_prompt[:2000]}\n\n"
            f"변형 조건:\n"
            f"- 도메인: {domain}\n"
            f"- 난이도: {level}\n"
            f"- 포맷: {fmt} 중심\n"
        )
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": PROLIFERATION_SYSTEM_PROMPT},
                {"role": "user", "content": user_msg},
            ],
        )
        content = response.choices[0].message.content

    return {
        "domain": domain,
        "level": level,
        "format": fmt,
        "content": content,
        "notion_title": notion_title,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


# ---------------------------------------------------------------------------
# Batch Proliferator (ThreadPoolExecutor)
# ---------------------------------------------------------------------------
def proliferate(
    base_prompt: str,
    target_count: int = 4,
    seed: Optional[int] = None,
    dry_run: bool = False,
    max_workers: int = 4,
) -> list[dict]:
    """
    Generate `target_count` prompt variants concurrently.

    Args:
        base_prompt  : Improved base prompt text.
        target_count : Number of variants to generate.
        seed         : Random seed for reproducible combo selection.
        dry_run      : Skip LLM calls.
        max_workers  : ThreadPoolExecutor concurrency limit.

    Returns:
        List of variant dicts sorted by domain name.
    """
    all_combos = list(
        itertools.product(
            PROLIFERATION_MATRIX["domains"],
            PROLIFERATION_MATRIX["levels"],
            PROLIFERATION_MATRIX["formats"],
        )
    )

    rng = random.Random(seed)
    selected = rng.sample(all_combos, min(target_count, len(all_combos)))

    print(f"\n[PE-2] 변형 생성 시작 — {len(selected)}개 | workers={max_workers}")
    results: list[dict] = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {
            executor.submit(
                _generate_single_variant, base_prompt, d, l, f, dry_run
            ): (d, l, f)
            for d, l, f in selected
        }
        for future in as_completed(future_map):
            combo = future_map[future]
            try:
                variant = future.result()
                results.append(variant)
                print(f"  [✓] {variant['notion_title']}")
            except Exception as exc:  # noqa: BLE001
                print(f"  [E] {combo} — {exc}")

    results.sort(key=lambda v: v["domain"])
    _save_variants(results)
    _write_json_log(results)
    return results


# ---------------------------------------------------------------------------
# Save Variants to Disk
# ---------------------------------------------------------------------------
def _save_variants(variants: list[dict]) -> None:
    """
    Save each variant as a .md file under prompts/variants/.
    Filename: PE-7_{domain_slug}_{level_slug}.md
    """
    for v in variants:
        slug_domain = v["domain"].replace(" ", "_")[:20]
        slug_level = v["level"].replace(" ", "_")[:10]
        filename = f"PE-7_{slug_domain}_{slug_level}.md"
        path = PROMPT_OUT_DIR / filename
        path.write_text(v["content"], encoding="utf-8")
        print(f"  [저장] {path}")


# ---------------------------------------------------------------------------
# JSON Log
# ---------------------------------------------------------------------------
def _write_json_log(variants: list[dict]) -> None:
    today = datetime.utcnow().strftime("%Y%m%d")
    log_path = LOG_DIR / f"pe2_proliferation_{today}.json"
    summary = [
        {
            k: v[k]
            for k in ("domain", "level", "format", "notion_title", "timestamp")
        }
        for v in variants
    ]
    log_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"  [로그] {log_path}")


# ---------------------------------------------------------------------------
# Matrix Info
# ---------------------------------------------------------------------------
def print_matrix_info() -> None:
    """Print available domains / levels / formats and total combo count."""
    total = (
        len(PROLIFERATION_MATRIX["domains"])
        * len(PROLIFERATION_MATRIX["levels"])
        * len(PROLIFERATION_MATRIX["formats"])
    )
    print("\n[PE-2] Proliferation Matrix")
    for key, vals in PROLIFERATION_MATRIX.items():
        print(f"  {key}: {vals}")
    print(f"  Total combos: {total}")


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="PE-2 Prompt Proliferator")
    parser.add_argument("input", nargs="?", help="Base prompt file (.md/.txt)")
    parser.add_argument("--count", type=int, default=4, help="Number of variants (default: 4)")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    parser.add_argument("--dry-run", action="store_true", help="Skip LLM calls")
    parser.add_argument("--workers", type=int, default=4, help="ThreadPoolExecutor workers")
    parser.add_argument("--matrix", action="store_true", help="Print matrix info and exit")
    args = parser.parse_args()

    if args.matrix:
        print_matrix_info()
        sys.exit(0)

    if not args.input:
        parser.print_help()
        sys.exit(0)

    base_text = Path(args.input).read_text(encoding="utf-8")
    variants = proliferate(
        base_text,
        target_count=args.count,
        seed=args.seed,
        dry_run=args.dry_run,
        max_workers=args.workers,
    )

    print(f"\n[완료] {len(variants)}개 변형 생성 → {PROMPT_OUT_DIR}/")
    for v in variants:
        print(f"  • {v['notion_title']}")
