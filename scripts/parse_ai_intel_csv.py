#!/usr/bin/env python3
"""
11-Section AI Intel CSV Parser → Entity Extractor
C-31 PE-AI Intelligence Library Pipeline
Generated: 2026-05-01
"""

import csv
import json
import re
import sys
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional

# ── 섹션 정의 (11개) ──
SECTION_MAP = {
    1:  "company_overview",
    2:  "product_portfolio",
    3:  "rd_investment",
    4:  "patent_landscape",
    5:  "supply_chain",
    6:  "financial_metrics",
    7:  "market_share",
    8:  "partnership_ecosystem",
    9:  "regulatory_compliance",
    10: "talent_headcount",
    11: "strategic_outlook",
}

@dataclass
class Entity:
    entity_id:    str
    entity_type:  str
    name:         str
    section:      int
    section_name: str
    attributes:   dict = field(default_factory=dict)
    relations:    list = field(default_factory=list)
    source_row:   int  = 0

def infer_type(name: str, section: int) -> str:
    tech_kw   = re.compile(r"HBM|GPU|TPU|LLM|DRAM|NAND|AI|ML|SoC|ASIC|\bIP\b", re.I)
    market_kw = re.compile(r"market|segment|region|TAM|SAM|SOM", re.I)
    person_kw = re.compile(r"CEO|CTO|CFO|Dr\.|Mr\.|Ms\.", re.I)
    if section in (2, 3, 4): return "TECHNOLOGY"
    if section in (7,):       return "MARKET"
    if section in (10,):      return "PERSON"
    if tech_kw.search(name):  return "TECHNOLOGY"
    if market_kw.search(name):return "MARKET"
    if person_kw.search(name):return "PERSON"
    if section in (1, 8):     return "COMPANY"
    return "COMPANY"

def parse_csv(csv_path: str) -> list:
    entities = []
    entity_counter = {}
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=2):
            raw_sec = row.get("section", row.get("Section", "0"))
            try:
                sec_num = int(str(raw_sec).strip())
            except ValueError:
                sec_num = 0
            sec_name = SECTION_MAP.get(sec_num, "unknown")
            name_col = next(
                (k for k in row if k.lower() in ("entity", "name", "company", "product", "entity_name")),
                None
            )
            if not name_col or not row.get(name_col, "").strip():
                continue
            name = row[name_col].strip()
            e_type = infer_type(name, sec_num)
            prefix = e_type[:3].upper()
            entity_counter[prefix] = entity_counter.get(prefix, 0) + 1
            eid = f"{prefix}-{entity_counter[prefix]:04d}"
            skip_cols = {name_col, "section", "Section"}
            attrs = {k.strip(): v.strip() for k, v in row.items()
                     if k not in skip_cols and v and v.strip()}
            rels = []
            for k, v in list(attrs.items()):
                if k.lower().startswith("rel_") or k.lower() in ("parent", "related_to"):
                    rels.append({"type": k.replace("rel_", "").upper(), "target": v})
                    del attrs[k]
            entities.append(Entity(
                entity_id=eid, entity_type=e_type, name=name,
                section=sec_num, section_name=sec_name,
                attributes=attrs, relations=rels, source_row=row_num,
            ))
    return entities

def batch_output(entities: list, out_json: str, out_csv: str):
    data = {
        "meta": {
            "version": "v1.0",
            "total_entities": len(entities),
            "sections_covered": sorted(set(e.section for e in entities)),
            "generated_at": "2026-05-01T10:46:00+09:00",
        },
        "entities": [asdict(e) for e in entities],
    }
    Path(out_json).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    if entities:
        with open(out_csv, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["entity_id", "entity_type", "name", "section", "section_name", "source_row"]
            import csv as _csv
            writer = _csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for e in entities:
                writer.writerow({
                    "entity_id": e.entity_id, "entity_type": e.entity_type,
                    "name": e.name, "section": e.section,
                    "section_name": e.section_name, "source_row": e.source_row,
                })
    print(f"[✓] 엔티티 추출 완료: {len(entities)}개 → {out_json}, {out_csv}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="11-Section AI Intel CSV → Entity Extractor")
    parser.add_argument("csv_input")
    parser.add_argument("--out-json", default="entities_extracted.json")
    parser.add_argument("--out-csv",  default="entities_batch.csv")
    args = parser.parse_args()
    entities = parse_csv(args.csv_input)
    batch_output(entities, args.out_json, args.out_csv)

if __name__ == "__main__":
    main()
