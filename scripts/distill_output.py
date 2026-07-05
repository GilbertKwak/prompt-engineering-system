#!/usr/bin/env python3
"""
distill_output.py — Prompt Output Distiller
===========================================
repowise 'distill' 패턴을 프롬프트 파이프라인에 이식.

역할:
  - 자동검증/자동개선 루프의 장황한 출력을 LLM 컨텍스트 효율적으로 압축
  - FAIL > WARN > PASS > INFO 우선순위로 필터링
  - [pe#XXXXX] 마커로 원본 로그 복원 가능
  - JSONL 아카이브: logs/PROMPT_DISTILL_LOG.jsonl
  - Notion-ready dict 반환 (PE Prompt Version Tracker DB 동기화용)

사용법:
  python scripts/distill_output.py --input <log_text_or_file> [--mode strict|normal|verbose]
  python scripts/distill_output.py --stdin < validation_output.txt
  python scripts/distill_output.py --test  # 자체 테스트 실행

연동:
  GitHub SSOT: GilbertKwak/prompt-engineering-system/scripts/distill_output.py
  Notion DB:   PE Prompt Version Tracker (Output Log 컬럼)
  Archive:     logs/PROMPT_DISTILL_LOG.jsonl
"""

import re
import sys
import json
import uuid
import hashlib
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ─── 상수 ────────────────────────────────────────────────────────────────────
VERSION = "1.0.0"
ARCHIVE_PATH = Path("logs/PROMPT_DISTILL_LOG.jsonl")
MARKER_PREFIX = "pe"

# 우선순위 레벨 (낮을수록 높은 우선순위 → 압축 후에도 반드시 보존)
PRIORITY = {
    "FAIL":    0,
    "ERROR":   0,
    "CRITICAL": 0,
    "WARN":    1,
    "WARNING": 1,
    "PASS":    2,
    "OK":      2,
    "SUCCESS": 2,
    "INFO":    3,
    "DEBUG":   4,
    "TRACE":   5,
}

# strict 모드: FAIL/WARN만 보존 (최고 압축률)
# normal 모드: FAIL/WARN/PASS 보존 (기본값)
# verbose 모드: 전체 보존 (압축 없음, 아카이브만)
MODE_THRESHOLD = {
    "strict":  1,   # priority <= 1 만 보존
    "normal":  2,   # priority <= 2 만 보존  (기본값)
    "verbose": 99,  # 전부 보존
}

# ─── 핵심 클래스 ─────────────────────────────────────────────────────────────

class PromptDistiller:
    """
    프롬프트 파이프라인 출력 압축기.
    repowise distill 패턴: 실패 우선 + 마커 시스템 + JSONL 아카이브.
    """

    def __init__(self, mode: str = "normal", archive: bool = True):
        self.mode = mode
        self.archive_enabled = archive
        self.threshold = MODE_THRESHOLD.get(mode, 2)
        self._session_id = self._gen_marker(8)

    # ── 마커 생성 ─────────────────────────────────────────────────────────────
    @staticmethod
    def _gen_marker(length: int = 5) -> str:
        """[pe#XXXXX] 형식의 UUID 기반 짧은 마커 생성."""
        return uuid.uuid4().hex[:length].upper()

    # ── 줄별 우선순위 파싱 ────────────────────────────────────────────────────
    def _parse_line_priority(self, line: str) -> int:
        """줄에서 우선순위 레벨 추출. 매칭 없으면 INFO(3) 반환."""
        upper = line.upper()
        for keyword, level in PRIORITY.items():
            # [FAIL], FAIL:, ✗ FAIL, × FAIL 등 다양한 패턴 커버
            if re.search(r'(?:^|[\[\s✗×])' + keyword + r'(?:[\]:\s]|$)', upper):
                return level
        # 특수 심볼 기반 폴백
        if any(sym in line for sym in ["✗", "×", "❌", "FAILED", "EXCEPTION"]):
            return 0  # FAIL
        if any(sym in line for sym in ["⚠", "!", "WARN"]):
            return 1  # WARN
        if any(sym in line for sym in ["✓", "✅", "PASS", "OK"]):
            return 2  # PASS
        return 3  # INFO 기본값

    # ── 메인 압축 로직 ────────────────────────────────────────────────────────
    def distill(
        self,
        raw_text: str,
        source_id: Optional[str] = None,
        prompt_id: Optional[str] = None,
    ) -> dict:
        """
        원본 텍스트를 압축하고 구조화된 결과 dict 반환.

        Returns:
            {
                'marker':        str,   # [pe#XXXXX] 복원 키
                'session_id':    str,   # 세션 고유 ID
                'timestamp':     str,   # ISO 8601 UTC
                'source_id':     str,   # 입력 파일명 또는 식별자
                'prompt_id':     str,   # 대상 프롬프트 ID
                'mode':          str,   # strict|normal|verbose
                'original_lines': int,  # 원본 줄 수
                'distilled_lines': int, # 압축 후 줄 수
                'compression_pct': float, # 압축률 %
                'token_estimate_original': int,
                'token_estimate_distilled': int,
                'fail_count':    int,
                'warn_count':    int,
                'pass_count':    int,
                'distilled_text': str,  # 실제 압축 결과
                'notion_ready':  dict,  # Notion DB 동기화용
                'status':        str,   # CLEAN|WARN|FAIL
            }
        """
        lines = raw_text.splitlines()
        marker = self._gen_marker(5)
        timestamp = datetime.now(timezone.utc).isoformat()

        # 줄별 분류
        categorized = []
        for line in lines:
            stripped = line.strip()
            if not stripped:  # 빈 줄 제거
                continue
            priority = self._parse_line_priority(stripped)
            categorized.append((priority, stripped))

        # 압축: 임계값 이하 우선순위만 보존
        kept = [(p, l) for p, l in categorized if p <= self.threshold]

        # 통계
        fail_count = sum(1 for p, _ in categorized if p == 0)
        warn_count = sum(1 for p, _ in categorized if p == 1)
        pass_count = sum(1 for p, _ in categorized if p == 2)

        original_lines = len(categorized)
        distilled_lines = len(kept)
        compression_pct = round(
            (1 - distilled_lines / original_lines) * 100, 1
        ) if original_lines > 0 else 0.0

        # 토큰 추정 (1 토큰 ≈ 4자 경험칙)
        token_est_orig = len(raw_text) // 4
        distilled_text_raw = "\n".join(l for _, l in kept)
        token_est_dist = len(distilled_text_raw) // 4

        # 헤더 + 마커 주입
        header = (
            f"# DISTILLED [{MARKER_PREFIX}#{marker}] "
            f"| mode={self.mode} "
            f"| {distilled_lines}/{original_lines} lines "
            f"| {compression_pct}% compressed "
            f"| FAIL={fail_count} WARN={warn_count} PASS={pass_count}"
        )

        # FAIL/WARN 섹션을 최상단에, PASS를 하단에 배치
        fail_lines = [l for p, l in kept if p == 0]
        warn_lines = [l for p, l in kept if p == 1]
        pass_lines = [l for p, l in kept if p == 2]
        other_lines = [l for p, l in kept if p > 2]

        sections = [header]
        if fail_lines:
            sections.append("\n## ❌ FAILURES")
            sections.extend(f"  {l}" for l in fail_lines)
        if warn_lines:
            sections.append("\n## ⚠️  WARNINGS")
            sections.extend(f"  {l}" for l in warn_lines)
        if pass_lines:
            sections.append("\n## ✅ PASSED")
            sections.extend(f"  {l}" for l in pass_lines)
        if other_lines:
            sections.append("\n## ℹ️  INFO")
            sections.extend(f"  {l}" for l in other_lines)

        distilled_text = "\n".join(sections)

        # 전체 상태 결정
        if fail_count > 0:
            status = "FAIL"
        elif warn_count > 0:
            status = "WARN"
        else:
            status = "CLEAN"

        # Notion-ready dict (PE Prompt Version Tracker DB 컬럼 매핑)
        notion_ready = {
            "Output Log": distilled_text[:2000],  # Notion 텍스트 컬럼 안전 길이
            "Distill Marker": f"[{MARKER_PREFIX}#{marker}]",
            "Compression %": compression_pct,
            "FAIL Count": fail_count,
            "WARN Count": warn_count,
            "Status": status,
            "Distill Mode": self.mode,
            "Timestamp": timestamp,
            "Token Saved": token_est_orig - token_est_dist,
        }
        if prompt_id:
            notion_ready["Prompt ID"] = prompt_id

        result = {
            "marker": f"[{MARKER_PREFIX}#{marker}]",
            "session_id": self._session_id,
            "timestamp": timestamp,
            "source_id": source_id or "stdin",
            "prompt_id": prompt_id or "",
            "mode": self.mode,
            "original_lines": original_lines,
            "distilled_lines": distilled_lines,
            "compression_pct": compression_pct,
            "token_estimate_original": token_est_orig,
            "token_estimate_distilled": token_est_dist,
            "token_saved": token_est_orig - token_est_dist,
            "fail_count": fail_count,
            "warn_count": warn_count,
            "pass_count": pass_count,
            "distilled_text": distilled_text,
            "notion_ready": notion_ready,
            "status": status,
            # 원본 보존 (아카이브용, 출력에는 포함 안 됨)
            "_raw_text_hash": hashlib.sha256(raw_text.encode()).hexdigest()[:16],
        }

        # JSONL 아카이브
        if self.archive_enabled:
            self._archive(result, raw_text)

        return result

    # ── 아카이브 ──────────────────────────────────────────────────────────────
    def _archive(self, result: dict, raw_text: str) -> None:
        """logs/PROMPT_DISTILL_LOG.jsonl 에 원본 + 메타 저장."""
        ARCHIVE_PATH.parent.mkdir(parents=True, exist_ok=True)
        archive_entry = {k: v for k, v in result.items() if k != "_raw_text_hash"}
        archive_entry["raw_text"] = raw_text  # 원본 전체 보존
        with open(ARCHIVE_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(archive_entry, ensure_ascii=False) + "\n")

    # ── 복원 ──────────────────────────────────────────────────────────────────
    @staticmethod
    def restore(marker: str, archive_path: Path = ARCHIVE_PATH) -> Optional[str]:
        """
        [pe#XXXXX] 마커로 원본 텍스트 복원.
        marker: '[pe#ABC12]' 또는 'ABC12' 모두 허용.
        """
        clean = marker.replace("[", "").replace("]", "").replace(f"{MARKER_PREFIX}#", "")
        if not archive_path.exists():
            print(f"[DISTILLER] Archive not found: {archive_path}")
            return None
        with open(archive_path, encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if clean.upper() in entry.get("marker", "").upper():
                        return entry.get("raw_text", "")
                except json.JSONDecodeError:
                    continue
        return None


# ─── 자체 테스트 ──────────────────────────────────────────────────────────────

SAMPLE_LOG = """
[INFO] Starting prompt validation pipeline v2.1
[INFO] Loading prompt: PE-SEMI-agent3-v4.2
[INFO] Checking instruction depth... depth=3
[PASS] Instruction depth: 3/4 ✓
[INFO] Checking purpose cohesion...
[PASS] Purpose cohesion: single role detected ✓
[INFO] Checking downstream coupling...
[WARN] Downstream coupling: 4 prompts linked (threshold=3)
[INFO] Checking churn rate...
[FAIL] Churn rate: 5 edits in 7 days (threshold=3) ✗
[INFO] Checking clone ratio...
[PASS] Clone ratio: 12% (threshold=20%) ✓
[INFO] Checking test coverage...
[WARN] Test coverage: 0 test cases found (minimum=1)
[INFO] Checking ambiguity score...
[PASS] Ambiguity score: 1 marker (threshold=2) ✓
[INFO] Checking blast radius...
[PASS] Blast radius: 3 prompts affected (threshold=5) ✓
[INFO] Computing health score...
[INFO] Health Score: 5.5/10
[FAIL] Health Score below threshold (6.5): PROLIFERATION TRIGGERED
[INFO] Spawning variant: PE-SEMI-agent3-v4.3
[INFO] Pipeline completed at 2026-07-05T14:07:00Z
"""


def run_self_test():
    """자체 테스트: 샘플 로그로 압축 결과 검증."""
    print("=" * 60)
    print(f"distill_output.py v{VERSION} — Self Test")
    print("=" * 60)

    for mode in ["strict", "normal", "verbose"]:
        d = PromptDistiller(mode=mode, archive=False)
        result = d.distill(SAMPLE_LOG, source_id="self_test", prompt_id="PE-SEMI-agent3-v4.2")
        print(f"\n[MODE={mode.upper()}]")
        print(f"  Lines: {result['original_lines']} → {result['distilled_lines']} ({result['compression_pct']}% compressed)")
        print(f"  Tokens: ~{result['token_estimate_original']} → ~{result['token_estimate_distilled']} (saved ~{result['token_saved']})")
        print(f"  Status: {result['status']} | FAIL={result['fail_count']} WARN={result['warn_count']} PASS={result['pass_count']}")
        print(f"  Marker: {result['marker']}")
        if mode == "normal":
            print("\n--- Distilled Output (normal mode) ---")
            print(result["distilled_text"])
            print("--------------------------------------")

    print("\n✅ Self test complete.")


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description=f"distill_output.py v{VERSION} — Prompt Output Distiller",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/distill_output.py --input validation.log
  python scripts/distill_output.py --stdin < output.txt
  python scripts/distill_output.py --restore pe#ABC12
  python scripts/distill_output.py --test
  python scripts/distill_output.py --input log.txt --mode strict --prompt-id PE-SEMI-v4
    """,
    )
    parser.add_argument("--input", "-i", help="입력 파일 경로 (없으면 --stdin 사용)")
    parser.add_argument("--stdin", action="store_true", help="표준 입력에서 읽기")
    parser.add_argument("--mode", choices=["strict", "normal", "verbose"], default="normal",
                        help="압축 모드 (기본값: normal)")
    parser.add_argument("--prompt-id", help="대상 프롬프트 ID (Notion 동기화용)")
    parser.add_argument("--no-archive", action="store_true", help="JSONL 아카이브 비활성화")
    parser.add_argument("--restore", metavar="MARKER", help="[pe#XXXXX] 마커로 원본 복원")
    parser.add_argument("--json", action="store_true", help="전체 결과를 JSON으로 출력")
    parser.add_argument("--test", action="store_true", help="자체 테스트 실행")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")

    args = parser.parse_args()

    # 자체 테스트
    if args.test:
        run_self_test()
        return

    # 복원 모드
    if args.restore:
        raw = PromptDistiller.restore(args.restore)
        if raw:
            print(raw)
        else:
            print(f"[DISTILLER] 마커 '{args.restore}'를 아카이브에서 찾을 수 없습니다.")
            sys.exit(1)
        return

    # 입력 소스 결정
    raw_text = ""
    source_id = "stdin"
    if args.input:
        path = Path(args.input)
        if not path.exists():
            print(f"[ERROR] 파일을 찾을 수 없습니다: {args.input}")
            sys.exit(1)
        raw_text = path.read_text(encoding="utf-8")
        source_id = path.name
    elif args.stdin or not sys.stdin.isatty():
        raw_text = sys.stdin.read()
    else:
        parser.print_help()
        sys.exit(0)

    if not raw_text.strip():
        print("[ERROR] 입력 텍스트가 비어있습니다.")
        sys.exit(1)

    # 실행
    distiller = PromptDistiller(
        mode=args.mode,
        archive=not args.no_archive,
    )
    result = distiller.distill(
        raw_text,
        source_id=source_id,
        prompt_id=args.prompt_id,
    )

    # 출력
    if args.json:
        output = {k: v for k, v in result.items() if not k.startswith("_")}
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(result["distilled_text"])
        print(f"\n{'─'*60}")
        print(f"Marker: {result['marker']} | Status: {result['status']}")
        print(f"Compression: {result['original_lines']} → {result['distilled_lines']} lines ({result['compression_pct']}% compressed)")
        print(f"Token estimate: ~{result['token_estimate_original']} → ~{result['token_estimate_distilled']} (saved ~{result['token_saved']})")
        if args.no_archive:
            print("[!] Archive disabled — original log not saved")
        else:
            print(f"Archive: {ARCHIVE_PATH}")


if __name__ == "__main__":
    main()
