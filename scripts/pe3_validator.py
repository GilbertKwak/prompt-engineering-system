#!/usr/bin/env python3
"""
PE-3 Validator — Prompt Quality Validator
v2.0: OpenAI v1+ 클라이언트, 스키마 검증, logging, is_pass, 환경변수, domain_fit 체크리스트
"""

import json
import logging
import os
import time

from openai import OpenAI, APITimeoutError, RateLimitError, APIError

# ─────────────────────────────────────────────
# 설정
# ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger("pe3_validator")

PASS_THRESHOLD: int = int(os.environ.get("PE3_PASS_THRESHOLD", 80))
MODEL: str          = os.environ.get("PE3_MODEL", "gpt-4o")
MAX_RETRIES: int    = int(os.environ.get("PE3_MAX_RETRIES", 2))

REQUIRED_KEYS = {"scores", "total", "is_pass", "weak_points", "improvement_hints"}
SCORE_KEYS    = {"clarity", "executability", "completeness", "reproducibility", "domain_fit"}

# ─────────────────────────────────────────────
# 검증 프롬프트
# ─────────────────────────────────────────────
VALIDATION_PROMPT = f"""
당신은 프롬프트 품질 심사관입니다.
아래 프롬프트를 5차원으로 채점하세요 (각 0~20점, 합계 100점).

채점 기준:
1. 명확성 (Clarity): 역할·목표·출력형식이 모호하지 않은가
2. 실행가능성 (Executability): 엔지니어가 바로 사용 가능한가
3. 완결성 (Completeness): 필수 섹션(역할/입력/출력/KPI/리스크)이 모두 있는가
4. 재현성 (Reproducibility): 동일 입력 → 동일 출력이 보장되는가
5. 도메인 적합성 (Domain Fit): 아래 체크리스트 기준으로 평가하라
   - [ ] HBM / 반도체 패키징 / 열관리 관련 기술 용어가 포함되어 있는가
   - [ ] 출력 형식이 Notion 또는 GitHub Markdown 파이프라인과 호환되는가
   - [ ] 한국어(KR) / 영어(EN) 병렬 출력 구조가 고려되어 있는가
   - [ ] CFD / FEA / TIM / sCO2 등 Gilbert 도메인 특화 용어가 적절히 사용되는가
   - [ ] 결과물이 PE-1 → PE-3 검증 체계와 연계 가능한가

출력 형식 (JSON strict — 키 이름 변경 금지):
{{
  "scores": {{
    "clarity": int,
    "executability": int,
    "completeness": int,
    "reproducibility": int,
    "domain_fit": int
  }},
  "total": int,
  "is_pass": bool,
  "weak_points": list[str],
  "improvement_hints": list[str]
}}

합격 기준: total >= {PASS_THRESHOLD}점이면 is_pass = true
주의: total은 반드시 5개 점수의 합과 일치해야 한다.
"""


# ─────────────────────────────────────────────
# 내부 함수
# ─────────────────────────────────────────────
def _validate_schema(result: dict) -> dict:
    """LLM 응답 스키마 무결성 검증 및 자동 교정."""
    missing_top = REQUIRED_KEYS - result.keys()
    if missing_top:
        raise ValueError(f"응답 최상위 키 누락: {missing_top}")

    missing_scores = SCORE_KEYS - result["scores"].keys()
    if missing_scores:
        raise ValueError(f"scores 필드 누락: {missing_scores}")

    for key in SCORE_KEYS:
        val = result["scores"][key]
        if not isinstance(val, int) or not (0 <= val <= 20):
            raise ValueError(f"scores.{key} 범위 오류: {val} (0~20 정수여야 함)")

    # total 크로스체크 — LLM 합산 오류 자동 교정
    computed = sum(result["scores"].values())
    if computed != result["total"]:
        logger.warning(
            "total 불일치 — LLM: %d, 실제합산: %d → 자동 교정",
            result["total"], computed,
        )
        result["total"] = computed

    # Python 측 재판정 (이중 보장)
    result["is_pass"] = result["total"] >= PASS_THRESHOLD
    return result


def _call_api(client: OpenAI, prompt_text: str) -> str:
    """지수 백오프 재시도 포함 API 호출. raw content 문자열 반환."""
    for attempt in range(MAX_RETRIES + 1):
        try:
            logger.info("API 요청 (시도 %d/%d)", attempt + 1, MAX_RETRIES + 1)
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": VALIDATION_PROMPT},
                    {"role": "user",   "content": f"검증 대상 프롬프트:\n\n{prompt_text}"},
                ],
                response_format={"type": "json_object"},
                timeout=30,
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
# 퍼블릭 API
# ─────────────────────────────────────────────
def validate_prompt(prompt_text: str) -> dict:
    """
    프롬프트를 PE-3 기준으로 검증한다.

    Returns:
        dict: scores, total, is_pass, weak_points, improvement_hints
    Raises:
        RuntimeError: API 재시도 초과 / 타임아웃
        ValueError: 스키마 불일치
    """
    client = OpenAI()
    raw = _call_api(client, prompt_text)

    try:
        result = json.loads(raw)
    except json.JSONDecodeError as e:
        logger.error("JSON 파싱 실패 — 원문: %s", raw[:200])
        raise ValueError(f"LLM 응답 JSON 파싱 실패: {e}") from e

    result = _validate_schema(result)

    if not result["is_pass"]:
        logger.warning(
            "[E-07] 검증 실패 — 점수: %d/100 | 약점: %s",
            result["total"], result["weak_points"],
        )
    else:
        logger.info("[OK] 검증 합격 — 점수: %d/100", result["total"])

    return result


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────
if __name__ == "__main__":
    import sys, argparse

    parser = argparse.ArgumentParser(description="PE-3 프롬프트 품질 검증기")
    parser.add_argument("file", nargs="?", help="검증할 프롬프트 파일 경로")
    args = parser.parse_args()

    prompt_text = (
        open(args.file, encoding="utf-8").read()
        if args.file
        else (print("프롬프트 입력 (Ctrl+D 종료):") or sys.stdin.read())
    )

    result = validate_prompt(prompt_text)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["is_pass"] else 1)
