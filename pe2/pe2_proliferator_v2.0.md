#!/usr/bin/env python3
"""
PE-2 Proliferator — Prompt Auto-Proliferation Engine
v2.0: OpenAI v1+ 클라이언트, logging 전면 교체, 지수 백오프 에러 핸들링,
      PE2_MODEL 환경변수 통일, mkdir 함수 내부 이동, 오타 수정
"""

from __future__ import annotations

import itertools
import json
import logging
import os
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Optional

from openai import OpenAI, RateLimitError, APITimeoutError, APIError

# ─────────────────────────────────────────────
# 설정
# ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger("pe2_proliferator")

MODEL: str          = os.environ.get("PE2_MODEL", "gpt-4o")
MAX_RETRIES: int    = int(os.environ.get("PE2_MAX_RETRIES", 2))
LOG_DIR: Path       = Path(os.environ.get("PE2_LOG_DIR", "logs"))
PROMPT_OUT_DIR: Path = Path(os.environ.get("PE2_OUT_DIR", "prompts/variants"))

# ─────────────────────────────────────────────
# Proliferation Matrix
# ─────────────────────────────────────────────
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
1. 원본의 7단계 구조 유지 (역할/목표/입력/출력/KPI/리스크/철학)
2. 도메인 특화 예시 코드 1개 이상 삽입
3. 난이도에 맞는 도구 스택으로 교체
4. 독립 실행 가능한 완결 프롬프트
5. 제목: [PE-7] {domain} {level}판 v1.0
6. 코드 스니펫 삭제 절대 금지
7. 추상적 문장 금지 — 실제 도구/API/커맨드 명시
"""


# ─────────────────────────────────────────────
# 내부 유틸
# ─────────────────────────────────────────────
def _ensure_dirs() -> None:
    """LOG_DIR, PROMPT_OUT_DIR 런타임 생성 (import 시점 실행 방지)."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    PROMPT_OUT_DIR.mkdir(parents=True, exist_ok=True)


def _call_api_with_retry(client: OpenAI, messages: list[dict]) -> str:
    """지수 백오프 재시도 포함 API 호출. raw content 문자열 반환."""
    for attempt in range(MAX_RETRIES + 1):
        try:
            logger.info("API 요청 (시도 %d/%d)", attempt + 1, MAX_RETRIES + 1)
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                timeout=60,
            )
            return response.choices[0].message.content

        except RateLimitError:
            wait = 2 ** attempt
            logger.warning("Rate Limit — %d초 후 재시도", wait)
            if attempt < MAX_RETRIES:
                time.sleep(wait)
            else:
                raise RuntimeError(f"Rate Limit 재시도 초과 ({MAX_RETRIES}회)")

        except APITimeoutError:
            raise RuntimeError("OpenAI API 타임아웃")

        except APIError as e:
            raise RuntimeError(f"OpenAI API 에러: {e}") from e


# ─────────────────────────────────────────────
# Single Variant Generator
# ─────────────────────────────────────────────
def _generate_single_variant(
    base_prompt: str,
    domain: str,
    level: str,
    fmt: str,
    dry_run: bool = False,
) -> dict:
    """
    단일 (domain, level, format) 조합에 대한 변형 프롬프트 생성.
    Returns dict: domain, level, format, content, notion_title, timestamp
    """
    notion_title = f"[PE-7] {domain[:12]} {level[:4]}판 v1.0"

    if dry_run:
        content = (
            f"# {notion_title}\n\n"
            f"[dry_run] 도메인: {domain} | 난이도: {level} | 포맷: {fmt}\n\n"
            + base_prompt[:500]
            + "\n..."
        )
        logger.info("[dry_run] %s", notion_title)
    else:
        client = OpenAI()  # OPENAI_API_KEY 환경변수 자동 탐지
        user_msg = (
            f"원본 프롬프트 (앞 2000자):\n{base_prompt[:2000]}\n\n"
            f"변형 조건:\n"
            f"- 도메인: {domain}\n"
            f"- 난이도: {level}\n"
            f"- 포맷: {fmt} 중심\n"
        )
        content = _call_api_with_retry(
            client,
            messages=[
                {"role": "system", "content": PROLIFERATION_SYSTEM_PROMPT},
                {"role": "user",   "content": user_msg},
            ],
        )

    return {
        "domain":       domain,
        "level":        level,
        "format":       fmt,
        "content":      content,
        "notion_title": notion_title,
        "timestamp":    datetime.utcnow().isoformat() + "Z",
    }


# ─────────────────────────────────────────────
# Batch Proliferator (ThreadPoolExecutor)
# ─────────────────────────────────────────────
def proliferate(
    base_prompt: str,
    target_count: int = 4,
    seed: Optional[int] = None,
    dry_run: bool = False,
    max_workers: int = 4,
) -> list[dict]:
    """
    target_count개의 변형 프롬프트를 병렬로 생성한다.

    Args:
        base_prompt  : PE-1 개선 완료된 베이스 프롬프트 전문
        target_count : 생성할 변형 수
        seed         : 재현 가능한 콤보 선택을 위한 랜덤 시드
        dry_run      : True이면 LLM 호출 스킵
        max_workers  : ThreadPoolExecutor 동시 실행 수

    Returns:
        domain 기준 정렬된 변형 dict 리스트
    """
    _ensure_dirs()

    all_combos = list(itertools.product(
        PROLIFERATION_MATRIX["domains"],
        PROLIFERATION_MATRIX["levels"],
        PROLIFERATION_MATRIX["formats"],
    ))

    rng = random.Random(seed)
    selected = rng.sample(all_combos, min(target_count, len(all_combos)))

    logger.info("[PE-2] 변형 생성 시작 — %d개 | workers=%d", len(selected), max_workers)
    results: list[dict] = []
    failed: list[tuple] = []

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
                logger.info("[✓] %s", variant["notion_title"])
            except Exception as exc:  # noqa: BLE001
                logger.error("[E] %s — %s", combo, exc)
                failed.append(combo)

    if failed:
        logger.warning("[W] 실패한 변형 %d개: %s", len(failed), failed)

    results.sort(key=lambda v: v["domain"])
    _save_variants(results)
    _write_json_log(results)

    logger.info("[PE-2] 완료 — 성공: %d / 실패: %d", len(results), len(failed))
    return results


# ─────────────────────────────────────────────
# Save Variants to Disk
# ─────────────────────────────────────────────
def _save_variants(variants: list[dict]) -> None:
    """각 변형을 prompts/variants/ 하위에 .md 파일로 저장."""
    for v in variants:
        slug_domain = v["domain"].replace(" ", "_")[:20]
        slug_level  = v["level"].replace(" ", "_")[:10]
        filename    = f"PE-7_{slug_domain}_{slug_level}.md"
        path        = PROMPT_OUT_DIR / filename
        path.write_text(v["content"], encoding="utf-8")
        logger.info("[저장] %s", path)


# ─────────────────────────────────────────────
# JSON Log
# ─────────────────────────────────────────────
def _write_json_log(variants: list[dict]) -> None:
    """실행 결과 요약을 logs/pe2_proliferation_{YYYYMMDD}.json으로 저장."""
    today    = datetime.utcnow().strftime("%Y%m%d")
    log_path = LOG_DIR / f"pe2_proliferation_{today}.json"
    summary  = [
        {k: v[k] for k in ("domain", "level", "format", "notion_title", "timestamp")}
        for v in variants
    ]
    log_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    logger.info("[로그] %s", log_path)


# ─────────────────────────────────────────────
# Matrix Info
# ─────────────────────────────────────────────
def print_matrix_info() -> None:
    """사용 가능한 도메인/레벨/포맷 및 전체 콤보 수 출력."""
    total = (
        len(PROLIFERATION_MATRIX["domains"])
        * len(PROLIFERATION_MATRIX["levels"])
        * len(PROLIFERATION_MATRIX["formats"])
    )
    logger.info("[PE-2] Proliferation Matrix — Total combos: %d", total)
    for key, vals in PROLIFERATION_MATRIX.items():
        logger.info("  %s: %s", key, vals)


# ─────────────────────────────────────────────
# CLI Entry Point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="PE-2 Prompt Proliferator")
    parser.add_argument("input",      nargs="?",         help="베이스 프롬프트 파일 (.md/.txt)")
    parser.add_argument("--count",    type=int, default=4,    help="생성할 변형 수 (기본: 4)")
    parser.add_argument("--seed",     type=int, default=None, help="재현용 랜덤 시드")
    parser.add_argument("--dry-run",  action="store_true",    help="LLM 호출 스킵")
    parser.add_argument("--workers",  type=int, default=4,    help="병렬 워커 수")
    parser.add_argument("--matrix",   action="store_true",    help="매트릭스 정보 출력 후 종료")
    args = parser.parse_args()

    if args.matrix:
        print_matrix_info()
        sys.exit(0)

    if not args.input:
        parser.print_help()
        sys.exit(0)

    base_text = Path(args.input).read_text(encoding="utf-8")
    variants  = proliferate(
        base_text,
        target_count=args.count,
        seed=args.seed,
        dry_run=args.dry_run,
        max_workers=args.workers,
    )

    logger.info("[완료] %d개 변형 생성 → %s/", len(variants), PROMPT_OUT_DIR)
    for v in variants:
        logger.info("  • %s", v["notion_title"])
    sys.exit(0 if variants else 1)
