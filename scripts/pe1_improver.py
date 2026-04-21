#!/usr/bin/env python3
"""
PE-1 Improver — Prompt Auto-Improvement Engine
v2.0: OpenAI v1+ 클라이언트, 에러 핸들링, 구조 검증, 버전 증분,
      logs/ 자동 생성, change_log 구조화, 인코딩 지정, 타입 힌트
"""

import datetime
import difflib
import json
import logging
import os
import re
import time
from pathlib import Path

from openai import OpenAI, APITimeoutError, RateLimitError, APIError

# ─────────────────────────────────────────────
# 설정
# ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger("pe1_improver")

MODEL: str       = os.environ.get("PE1_MODEL", "gpt-4o")
MAX_RETRIES: int = int(os.environ.get("PE1_MAX_RETRIES", 2))
LOG_DIR: Path    = Path(os.environ.get("PE1_LOG_DIR", "logs"))

# ─────────────────────────────────────────────
# 개선 프롬프트
# ─────────────────────────────────────────────
IMPROVEMENT_PROMPT = """
당신은 프롬프트 개선 전문가입니다.

작업:
1. 아래 원본 프롬프트의 약점을 분석
2. 개선 힌트를 반영하여 섹션 단위로 재작성
3. 원본 구조(섹션 순서·헤더명)는 반드시 유지 — 헤더 삭제 절대 금지
4. 코드 스니펫은 보강만 허용 (삭제 금지)
5. 출력: 완전한 마크다운 프롬프트 전문

규칙:
- 추상적 문장 → 구체적 코드/예시로 교체
- 누락 섹션 → 템플릿 기반 자동 보충
- 버전 태그(vX.Y)는 절대 삭제하지 말 것 (Python이 직접 증분 처리함)
"""


# ─────────────────────────────────────────────
# 내부 유틸
# ─────────────────────────────────────────────
def _bump_version(text: str) -> str:
    """마크다운 내 첫 번째 'vX.Y' 패턴을 찾아 minor +1 증분."""
    def increment(m: re.Match) -> str:
        return f"v{m.group(1)}.{int(m.group(2)) + 1}"
    result, count = re.subn(r'v(\d+)\.(\d+)', increment, text, count=1)
    if count == 0:
        logger.warning("버전 태그(vX.Y) 미발견 — 증분 스킵")
    return result


def _check_structure(original: str, improved: str) -> list[str]:
    """원본 헤더(##, ###)가 개선본에 모두 존재하는지 검증. 누락 헤더 반환."""
    orig_headers = set(re.findall(r'^#{1,3} .+', original, re.MULTILINE))
    impr_headers = set(re.findall(r'^#{1,3} .+', improved, re.MULTILINE))
    return sorted(orig_headers - impr_headers)


def _call_api(client: OpenAI, context: str) -> str:
    """지수 백오프 재시도 포함 API 호출. raw content 문자열 반환."""
    for attempt in range(MAX_RETRIES + 1):
        try:
            logger.info("API 요청 (시도 %d/%d)", attempt + 1, MAX_RETRIES + 1)
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": IMPROVEMENT_PROMPT},
                    {"role": "user",   "content": context},
                ],
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


def _save_diff(before: str, after: str, diff_lines: list[str]) -> Path:
    """diff를 logs/ 디렉토리에 저장. 저장 경로 반환."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)  # 디렉토리 자동 생성
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = LOG_DIR / f"improvement_{ts}.diff"
    with open(log_path, "w", encoding="utf-8") as f:  # 인코딩 명시
        f.write("\n".join(diff_lines))
    logger.info("diff 저장 완료: %s (%d lines)", log_path, len(diff_lines))
    return log_path


# ─────────────────────────────────────────────
# 퍼블릭 API
# ─────────────────────────────────────────────
def improve_prompt(
    original: str,
    weak_points: list[str],
    hints: list[str],
) -> dict[str, object]:
    """
    원본 프롬프트를 약점·힌트 기반으로 자동 개선한다.

    Args:
        original:    원본 프롬프트 마크다운 전문
        weak_points: PE-3 검증에서 도출된 약점 목록
        hints:       PE-3 검증에서 도출된 개선 방향 목록

    Returns:
        {
          "improved_prompt": str,          # 개선된 프롬프트 전문
          "change_log": dict,              # 구조화된 변경 이력
          "missing_sections": list[str],   # 누락 감지된 섹션 (경고용)
          "diff_path": str,                # 저장된 diff 파일 경로
        }

    Raises:
        RuntimeError: API 재시도 초과 / 타임아웃
    """
    client = OpenAI()

    context = (
        f"원본 프롬프트:\n{original}\n\n"
        + f"약점 목록:\n" + "\n".join(f"- {w}" for w in weak_points) + "\n\n"
        + f"개선 방향:\n" + "\n".join(f"- {h}" for h in hints)
    )

    improved_raw = _call_api(client, context)

    # 버전 증분 (Python 직접 처리)
    improved = _bump_version(improved_raw)

    # 구조 무결성 검증
    missing = _check_structure(original, improved)
    if missing:
        logger.warning("[W-01] 섹션 누락 감지 (%d개): %s", len(missing), missing)
    else:
        logger.info("구조 검증 통과 — 헤더 전부 보존됨")

    # Diff 생성 및 저장
    diff_lines = list(difflib.unified_diff(
        original.splitlines(),
        improved.splitlines(),
        fromfile="original",
        tofile="improved",
        lineterm="",
    ))
    diff_path = _save_diff(original, improved, diff_lines)

    # 구조화된 change_log
    change_log = {
        "summary": f"PE-1 자동개선 — {len(weak_points)}개 약점 처리",
        "weak_points_addressed": weak_points,
        "hints_applied": hints,
        "diff_lines_total": len(diff_lines),
        "missing_sections": missing,
        "diff_path": str(diff_path),
        "timestamp": datetime.datetime.now().isoformat(),
        "model": MODEL,
    }

    logger.info(
        "[OK] 개선 완료 — diff %d lines | 누락섹션 %d개",
        len(diff_lines), len(missing),
    )

    return {
        "improved_prompt": improved,
        "change_log": change_log,
        "missing_sections": missing,
        "diff_path": str(diff_path),
    }


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────
if __name__ == "__main__":
    import sys, argparse

    parser = argparse.ArgumentParser(description="PE-1 프롬프트 자동 개선기")
    parser.add_argument("file",       help="원본 프롬프트 파일 경로 (.md)")
    parser.add_argument("--weak",     nargs="+", default=[], metavar="WEAK",
                        help="약점 항목 (공백 구분)")
    parser.add_argument("--hints",    nargs="+", default=[], metavar="HINT",
                        help="개선 힌트 (공백 구분)")
    parser.add_argument("--pe3-json", metavar="FILE",
                        help="pe3_validator 출력 JSON 파일 (--weak/--hints 대체)")
    args = parser.parse_args()

    # PE-3 결과 JSON에서 자동 로드
    if args.pe3_json:
        with open(args.pe3_json, encoding="utf-8") as f:
            pe3 = json.load(f)
        weak_points = pe3.get("weak_points", [])
        hints       = pe3.get("improvement_hints", [])
    else:
        weak_points = args.weak
        hints       = args.hints

    with open(args.file, encoding="utf-8") as f:
        original = f.read()

    result = improve_prompt(original, weak_points, hints)

    # 개선된 프롬프트를 {stem}_improved.md 로 저장
    out_path = Path(args.file).stem + "_improved.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(result["improved_prompt"])

    print(json.dumps(result["change_log"], ensure_ascii=False, indent=2))
    logger.info("개선 결과 저장: %s", out_path)
    sys.exit(0 if not result["missing_sections"] else 1)
