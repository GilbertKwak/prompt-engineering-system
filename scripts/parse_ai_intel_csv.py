#!/usr/bin/env python3
"""
Segment A — C-31 AI Intelligence Library CSV Parser
====================================================
File   : scripts/parse_ai_intel_csv.py
Version: 1.0.0
Created: 2026-05-01
Author : GilbertKwak / prompt-engineering-system

Purpose
-------
글로벌 AI 기술 인텔리전스 데이터를 담은 CSV 파일을 파싱하여
1) 정합성 검증 (schema validation)
2) 정규화 (field normalisation)
3) JSON → knowledge graph 적재 준비
4) Notion DB 업서트용 payload 생성

Expected CSV schema
-------------------
date, category, company, title, summary, source_url,
impact_score, region, tags, raw_signal

Usage
-----
# 기본 실행
python scripts/parse_ai_intel_csv.py --input data/ai_intel.csv

# 출력 경로 지정
python scripts/parse_ai_intel_csv.py \
    --input  data/ai_intel.csv \
    --output output/ai_intel_parsed.json \
    --notion           # Notion DB 업서트 payload 도 함께 생성

# 검증만 수행 (dry-run)
python scripts/parse_ai_intel_csv.py --input data/ai_intel.csv --validate-only

Environment variables (optional)
---------------------------------
NOTION_TOKEN    : Notion integration token
NOTION_DB_ID    : C-31 Notion database ID
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
REQUIRED_COLUMNS: list[str] = [
    "date", "category", "company", "title", "summary",
    "source_url", "impact_score", "region", "tags", "raw_signal",
]

VALID_CATEGORIES: set[str] = {
    "LLM", "Semiconductor", "Infrastructure", "Application",
    "Policy", "Investment", "Research", "Other",
}

VALID_REGIONS: set[str] = {
    "US", "CN", "EU", "KR", "JP", "IN", "Global", "Other",
}

MAX_SUMMARY_LEN: int = 500
MAX_TITLE_LEN: int = 200

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------
@dataclass
class AIIntelRecord:
    """정규화된 AI 인텔리전스 단일 레코드."""
    date: str                          # ISO-8601 YYYY-MM-DD
    category: str
    company: str
    title: str
    summary: str
    source_url: str
    impact_score: float                # 0.0 – 10.0
    region: str
    tags: list[str]
    raw_signal: str
    # 파서가 추가하는 메타
    parsed_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    row_index: int = 0
    warnings: list[str] = field(default_factory=list)

    def to_notion_payload(self, db_id: str) -> dict[str, Any]:
        """Notion DB 업서트용 payload 반환 (pages.create 형식)."""
        return {
            "parent": {"database_id": db_id},
            "properties": {
                "Title": {
                    "title": [{"text": {"content": self.title[:MAX_TITLE_LEN]}}]
                },
                "Date": {"date": {"start": self.date}},
                "Category": {"select": {"name": self.category}},
                "Company": {
                    "rich_text": [{"text": {"content": self.company}}]
                },
                "Summary": {
                    "rich_text": [{"text": {"content": self.summary[:MAX_SUMMARY_LEN]}}]
                },
                "Source URL": {"url": self.source_url or None},
                "Impact Score": {"number": round(self.impact_score, 2)},
                "Region": {"select": {"name": self.region}},
                "Tags": {
                    "multi_select": [{"name": t.strip()} for t in self.tags if t.strip()]
                },
                "Raw Signal": {
                    "rich_text": [{"text": {"content": self.raw_signal[:2000]}}]
                },
            },
        }


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------
def _parse_date(value: str, row: int) -> tuple[str, list[str]]:
    """날짜 문자열을 ISO-8601로 정규화. 파싱 실패 시 경고 반환."""
    warnings: list[str] = []
    formats = ["%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%m/%d/%Y", "%Y%m%d"]
    for fmt in formats:
        try:
            return datetime.strptime(value.strip(), fmt).strftime("%Y-%m-%d"), warnings
        except ValueError:
            continue
    warnings.append(f"row {row}: 날짜 파싱 실패 '{value}' → 오늘 날짜로 대체")
    return date.today().isoformat(), warnings


def _parse_impact_score(value: str, row: int) -> tuple[float, list[str]]:
    """impact_score를 float로 변환하고 범위를 0–10으로 클램핑."""
    warnings: list[str] = []
    try:
        score = float(value.strip())
    except (ValueError, AttributeError):
        warnings.append(f"row {row}: impact_score 변환 실패 '{value}' → 0.0")
        return 0.0, warnings
    if not 0.0 <= score <= 10.0:
        warnings.append(f"row {row}: impact_score 범위 초과 {score} → clamp(0,10)")
        score = max(0.0, min(10.0, score))
    return score, warnings


def _parse_tags(value: str) -> list[str]:
    """세미콜론 또는 쉼표로 구분된 태그 문자열을 리스트로 변환."""
    sep = ";" if ";" in value else ","
    return [t.strip() for t in value.split(sep) if t.strip()]


def _validate_url(url: str, row: int) -> list[str]:
    """기본적인 URL 형식 검증."""
    warnings: list[str] = []
    if url and not re.match(r"^https?://", url.strip()):
        warnings.append(f"row {row}: source_url 형식 불명확 '{url}'")
    return warnings


def _normalise_category(value: str, row: int) -> tuple[str, list[str]]:
    """카테고리를 유효 집합에 매핑; 없으면 'Other' 처리."""
    warnings: list[str] = []
    cat = value.strip().title()
    # 단순 키워드 매핑
    alias: dict[str, str] = {
        "Ai": "LLM", "Llm": "LLM", "Gpu": "Semiconductor",
        "Chip": "Semiconductor", "Cloud": "Infrastructure",
        "Regulation": "Policy", "VC": "Investment",
    }
    cat = alias.get(cat, cat)
    if cat not in VALID_CATEGORIES:
        warnings.append(f"row {row}: 미지 category '{cat}' → 'Other'")
        cat = "Other"
    return cat, warnings


def _normalise_region(value: str, row: int) -> tuple[str, list[str]]:
    """지역 코드를 유효 집합에 매핑."""
    warnings: list[str] = []
    reg = value.strip().upper()
    alias: dict[str, str] = {
        "KOREA": "KR", "SOUTH KOREA": "KR", "CHINA": "CN",
        "UNITED STATES": "US", "USA": "US", "EUROPE": "EU",
        "JAPAN": "JP", "INDIA": "IN",
    }
    reg = alias.get(reg, reg)
    if reg not in VALID_REGIONS:
        warnings.append(f"row {row}: 미지 region '{reg}' → 'Global'")
        reg = "Global"
    return reg, warnings


# ---------------------------------------------------------------------------
# Core parser
# ---------------------------------------------------------------------------
class AIIntelCSVParser:
    """
    CSV 파싱 파이프라인:
    load → validate_schema → parse_rows → report
    """

    def __init__(self, filepath: str | Path, encoding: str = "utf-8-sig") -> None:
        self.filepath = Path(filepath)
        self.encoding = encoding
        self.records: list[AIIntelRecord] = []
        self.errors: list[str] = []
        self.all_warnings: list[str] = []

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------
    def run(self) -> list[AIIntelRecord]:
        """파싱 전체 파이프라인 실행."""
        log.info("📂 입력 파일: %s", self.filepath)
        rows = self._load()
        if not rows:
            return []
        self._validate_schema(rows[0])
        if self.errors:
            raise ValueError(f"스키마 오류:\n" + "\n".join(self.errors))
        self._parse_rows(rows)
        self._report()
        return self.records

    # ------------------------------------------------------------------
    # Internal steps
    # ------------------------------------------------------------------
    def _load(self) -> list[dict[str, str]]:
        if not self.filepath.exists():
            self.errors.append(f"파일 없음: {self.filepath}")
            return []
        try:
            with self.filepath.open(encoding=self.encoding, newline="") as fh:
                reader = csv.DictReader(fh)
                rows = list(reader)
            log.info("✅ %d 행 로드 완료", len(rows))
            return rows
        except Exception as exc:
            self.errors.append(f"파일 읽기 오류: {exc}")
            return []

    def _validate_schema(self, sample_row: dict[str, str]) -> None:
        """헤더에 필수 컬럼이 모두 있는지 확인."""
        actual = set(sample_row.keys())
        missing = set(REQUIRED_COLUMNS) - actual
        if missing:
            self.errors.append(f"누락된 컬럼: {sorted(missing)}")
        else:
            log.info("✅ 스키마 검증 통과")

    def _parse_rows(self, rows: list[dict[str, str]]) -> None:
        """각 행을 AIIntelRecord로 변환."""
        for i, row in enumerate(rows, start=2):  # row 2 = CSV 2번째 줄 (1은 헤더)
            warnings: list[str] = []

            # --- 날짜 ---
            date_str, w = _parse_date(row.get("date", ""), i)
            warnings.extend(w)

            # --- 카테고리 ---
            category, w = _normalise_category(row.get("category", ""), i)
            warnings.extend(w)

            # --- 지역 ---
            region, w = _normalise_region(row.get("region", ""), i)
            warnings.extend(w)

            # --- impact_score ---
            score, w = _parse_impact_score(row.get("impact_score", "0"), i)
            warnings.extend(w)

            # --- URL ---
            url = row.get("source_url", "").strip()
            warnings.extend(_validate_url(url, i))

            # --- tags ---
            tags = _parse_tags(row.get("tags", ""))

            # --- 텍스트 필드 ---
            title = row.get("title", "").strip()[:MAX_TITLE_LEN]
            summary = row.get("summary", "").strip()[:MAX_SUMMARY_LEN]
            company = row.get("company", "").strip()
            raw_signal = row.get("raw_signal", "").strip()

            if not title:
                warnings.append(f"row {i}: title 비어있음")

            record = AIIntelRecord(
                date=date_str,
                category=category,
                company=company,
                title=title,
                summary=summary,
                source_url=url,
                impact_score=score,
                region=region,
                tags=tags,
                raw_signal=raw_signal,
                row_index=i,
                warnings=warnings,
            )
            self.records.append(record)
            self.all_warnings.extend(warnings)

        log.info("✅ %d 레코드 파싱 완료 (경고 %d건)", len(self.records), len(self.all_warnings))

    def _report(self) -> None:
        if self.all_warnings:
            log.warning("⚠️  파싱 경고 목록:")
            for w in self.all_warnings:
                log.warning("   %s", w)
        else:
            log.info("🎉 경고 없음 — 완전한 파싱 완료")


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------
def write_json(records: list[AIIntelRecord], output_path: str | Path) -> None:
    """파싱 결과를 JSON 파일로 저장."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = [asdict(r) for r in records]
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("💾 JSON 저장 완료: %s (%d 레코드)", output_path, len(records))


def write_notion_payloads(records: list[AIIntelRecord], output_path: str | Path, db_id: str) -> None:
    """Notion pages.create 형식의 payload 배열을 JSON으로 저장."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payloads = [r.to_notion_payload(db_id) for r in records]
    output_path.write_text(json.dumps(payloads, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("📤 Notion payload 저장 완료: %s (%d 항목)", output_path, len(payloads))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="C-31 AI Intelligence Library — Segment A CSV Parser",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--input",  "-i", required=True, help="입력 CSV 경로")
    p.add_argument("--output", "-o", default="output/ai_intel_parsed.json",
                   help="출력 JSON 경로 (기본: output/ai_intel_parsed.json)")
    p.add_argument("--notion", action="store_true",
                   help="Notion payload JSON 도 함께 생성")
    p.add_argument("--notion-db-id", default=os.getenv("NOTION_DB_ID", ""),
                   help="Notion database ID (환경변수 NOTION_DB_ID 우선)")
    p.add_argument("--validate-only", action="store_true",
                   help="파싱 및 검증만 수행, 파일 출력 없음")
    p.add_argument("--encoding", default="utf-8-sig",
                   help="CSV 인코딩 (기본: utf-8-sig)")
    p.add_argument("--log-level", default="INFO",
                   choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                   help="로그 레벨 (기본: INFO)")
    return p


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    logging.getLogger().setLevel(args.log_level)

    # 파싱 실행
    csv_parser = AIIntelCSVParser(args.input, encoding=args.encoding)
    try:
        records = csv_parser.run()
    except ValueError as exc:
        log.error("❌ 파싱 중단: %s", exc)
        sys.exit(1)

    if args.validate_only:
        log.info("--validate-only 모드: 파일 출력 생략")
        sys.exit(0)

    # 기본 JSON 출력
    write_json(records, args.output)

    # Notion payload 출력
    if args.notion:
        if not args.notion_db_id:
            log.warning("⚠️  --notion 플래그 활성화됐으나 NOTION_DB_ID가 없음")
        notion_out = Path(args.output).with_suffix("") + "_notion_payloads.json"
        write_notion_payloads(records, notion_out, args.notion_db_id)

    log.info("✅ Segment A 완료 — 총 %d 레코드 처리", len(records))


if __name__ == "__main__":
    main()
