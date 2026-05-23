#!/usr/bin/env python3
"""
generate_word.py — KM-PIPE Document Agent (A6)
Knowledge-to-Output Pipeline v3.0

Usage:
  python generate_word.py --input <json_file> --output <output.docx>
  python generate_word.py --title "Report Title" --content "..." --output report.docx

Part of: engines/KM-PIPE_knowledge-output-pipeline/
Linked engines: PE-1, PE-2, PE-3
Notion ref: T-09 > PE-IP > KM-PIPE-MASTER-v3.0
GitHub: engines/KM-PIPE_knowledge-output-pipeline/generate_word.py
Author: GilbertKwak (KM-PIPE v3.0)
Date: 2026-05-23
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    from docx import Document
    from docx.shared import Inches, Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.style import WD_STYLE_TYPE
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
except ImportError:
    print("[ERROR] python-docx not installed. Run: pip install python-docx")
    sys.exit(1)


# ─────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────
VERSION = "3.0.0"
KM_PIPE_ENGINE = "KM-PIPE-A6-DocumentAgent"
DEFAULT_AUTHOR = "GilbertKwak · KM-PIPE v3.0"
DEFAULT_DPI = 300

# Color palette (Tufte-inspired: neutral, minimal)
COLOR_HEADING1 = RGBColor(0x1A, 0x1A, 0x2E)  # Near-black
COLOR_HEADING2 = RGBColor(0x16, 0x21, 0x3E)  # Dark navy
COLOR_HEADING3 = RGBColor(0x0F, 0x3E, 0x60)  # Deep teal
COLOR_CAPTION = RGBColor(0x55, 0x55, 0x55)   # Gray
COLOR_TABLE_HEADER = RGBColor(0x1A, 0x1A, 0x2E)
COLOR_TABLE_HEADER_TEXT = RGBColor(0xFF, 0xFF, 0xFF)
COLOR_ACCENT = RGBColor(0x01, 0x69, 0x6F)    # Hydra Teal (Nexus)


# ─────────────────────────────────────────────────────────
# DOCUMENT STYLER
# ─────────────────────────────────────────────────────────
class DocumentStyler:
    """Apply Tufte-inspired clean styles to python-docx Document."""

    def __init__(self, doc: Document):
        self.doc = doc
        self._setup_default_style()

    def _setup_default_style(self):
        style = self.doc.styles["Normal"]
        font = style.font
        font.name = "Calibri"
        font.size = Pt(11)
        para_fmt = style.paragraph_format
        para_fmt.space_after = Pt(6)
        para_fmt.line_spacing = Pt(16)

    def add_title(self, text: str):
        para = self.doc.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = para.add_run(text)
        run.bold = True
        run.font.size = Pt(22)
        run.font.color.rgb = COLOR_HEADING1
        run.font.name = "Calibri"
        self.doc.add_paragraph()  # spacing

    def add_heading(self, text: str, level: int = 1):
        para = self.doc.add_paragraph()
        run = para.add_run(text)
        run.bold = True
        if level == 1:
            run.font.size = Pt(16)
            run.font.color.rgb = COLOR_HEADING1
            para.paragraph_format.space_before = Pt(18)
        elif level == 2:
            run.font.size = Pt(13)
            run.font.color.rgb = COLOR_HEADING2
            para.paragraph_format.space_before = Pt(12)
        else:
            run.font.size = Pt(11)
            run.font.color.rgb = COLOR_HEADING3
            para.paragraph_format.space_before = Pt(8)
        run.font.name = "Calibri"

    def add_body(self, text: str):
        para = self.doc.add_paragraph(text)
        para.paragraph_format.space_after = Pt(8)
        for run in para.runs:
            run.font.name = "Calibri"
            run.font.size = Pt(11)

    def add_abstract(self, text: str):
        """Boxed abstract with light background."""
        self.add_heading("Abstract", level=2)
        para = self.doc.add_paragraph(text)
        para.paragraph_format.left_indent = Inches(0.4)
        para.paragraph_format.right_indent = Inches(0.4)
        para.paragraph_format.space_after = Pt(12)
        for run in para.runs:
            run.font.name = "Calibri"
            run.font.size = Pt(10.5)
            run.font.italic = True

    def add_bullet_list(self, items: list, label: str = ""):
        if label:
            self.add_heading(label, level=3)
        for item in items:
            para = self.doc.add_paragraph(style="List Bullet")
            run = para.add_run(str(item))
            run.font.name = "Calibri"
            run.font.size = Pt(11)

    def add_table(self, headers: list, rows: list, caption: str = ""):
        """Tufte-style table: minimal borders, no decorative lines."""
        if caption:
            cap_para = self.doc.add_paragraph()
            cap_run = cap_para.add_run(f"Table: {caption}")
            cap_run.italic = True
            cap_run.font.size = Pt(9)
            cap_run.font.color.rgb = COLOR_CAPTION

        table = self.doc.add_table(rows=1, cols=len(headers))
        table.style = "Table Grid"

        # Header row
        hdr_cells = table.rows[0].cells
        for i, header in enumerate(headers):
            hdr_cells[i].text = str(header)
            hdr_para = hdr_cells[i].paragraphs[0]
            hdr_run = hdr_para.runs[0] if hdr_para.runs else hdr_para.add_run(str(header))
            hdr_run.bold = True
            hdr_run.font.color.rgb = COLOR_TABLE_HEADER_TEXT
            hdr_run.font.size = Pt(10)
            # Set header cell background
            tc = hdr_cells[i]._tc
            tcPr = tc.get_or_add_tcPr()
            shd = OxmlElement('w:shd')
            shd.set(qn('w:val'), 'clear')
            shd.set(qn('w:color'), 'auto')
            shd.set(qn('w:fill'), '1A1A2E')
            tcPr.append(shd)

        # Data rows
        for row_data in rows:
            row_cells = table.add_row().cells
            for i, cell_val in enumerate(row_data):
                row_cells[i].text = str(cell_val)
                for para in row_cells[i].paragraphs:
                    for run in para.runs:
                        run.font.size = Pt(10)

        self.doc.add_paragraph()  # spacing after table

    def add_image_placeholder(self, position_label: str, caption: str = ""):
        """Insert a visible placeholder for chart images."""
        para = self.doc.add_paragraph()
        run = para.add_run(f"[CHART PLACEHOLDER — {position_label}]")
        run.bold = True
        run.font.color.rgb = COLOR_ACCENT
        run.font.size = Pt(10)
        if caption:
            cap_para = self.doc.add_paragraph()
            cap_run = cap_para.add_run(f"Figure: {caption}")
            cap_run.italic = True
            cap_run.font.size = Pt(9)
            cap_run.font.color.rgb = COLOR_CAPTION

    def add_image(self, image_path: str, caption: str = "", width_inches: float = 5.5):
        """Insert actual image if path exists."""
        if os.path.exists(image_path):
            self.doc.add_picture(image_path, width=Inches(width_inches))
            if caption:
                cap_para = self.doc.add_paragraph()
                cap_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                cap_run = cap_para.add_run(f"Figure: {caption}")
                cap_run.italic = True
                cap_run.font.size = Pt(9)
                cap_run.font.color.rgb = COLOR_CAPTION
        else:
            self.add_image_placeholder(image_path, caption)

    def add_references(self, refs: list):
        self.add_heading("References", level=1)
        for i, ref in enumerate(refs, 1):
            para = self.doc.add_paragraph()
            run = para.add_run(f"[{i}] {ref}")
            run.font.size = Pt(10)
            run.font.name = "Calibri"
            para.paragraph_format.left_indent = Inches(0.3)

    def add_footer_metadata(self, meta: dict):
        """Add metadata footer: generated_by, date, pe_score."""
        self.doc.add_paragraph()
        footer_text = (
            f"Generated by: {meta.get('generated_by', DEFAULT_AUTHOR)} | "
            f"Date: {meta.get('date', datetime.now().strftime('%Y-%m-%d'))} | "
            f"PE-Score: {meta.get('pe_score', 'N/A')} | "
            f"KM-PIPE v{VERSION}"
        )
        para = self.doc.add_paragraph(footer_text)
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in para.runs:
            run.font.size = Pt(8)
            run.font.color.rgb = COLOR_CAPTION
            run.italic = True


# ─────────────────────────────────────────────────────────
# CORE GENERATOR
# ─────────────────────────────────────────────────────────
class WordDocumentGenerator:
    """
    A6 DocumentAgent — generates Word .docx from KM-PIPE JSON payload.
    Supports both full pipeline JSON (from km_pipe_runner) and
    simple title+content mode.
    """

    def __init__(self, verbose: bool = True):
        self.verbose = verbose

    def _log(self, msg: str):
        if self.verbose:
            print(f"[A6-DocAgent] {msg}")

    def from_json(self, payload: dict, output_path: str) -> str:
        """Generate Word doc from full KM-PIPE JSON payload."""
        self._log(f"Building document from pipeline payload...")
        doc = Document()
        styler = DocumentStyler(doc)

        # ── Title
        notion = payload.get("notion_data", {})
        word_struct = payload.get("word_doc_structure", {})
        viz = payload.get("visualization", {})
        insights = payload.get("insights", {})

        title = word_struct.get("title") or notion.get("title", "Untitled Report")
        styler.add_title(title)

        # ── Abstract
        abstract = word_struct.get("abstract") or notion.get("summary", "")
        if abstract:
            styler.add_abstract(abstract)

        # ── Key Points
        key_points = notion.get("key_points", [])
        if key_points:
            styler.add_bullet_list(key_points, label="Key Points")

        # ── Main Sections
        sections = word_struct.get("sections", [])
        image_slots = word_struct.get("image_placeholders", [])
        chart_paths = self._collect_chart_paths(output_path)

        for i, section in enumerate(sections):
            heading = section.get("heading", f"Section {i+1}")
            content = section.get("content", "")
            level = section.get("level", 2)

            styler.add_heading(heading, level=level)
            if content:
                styler.add_body(content)

            # Insert chart if slot exists for this section
            slot_key = f"after_section_{i+1}"
            matching_slot = next(
                (s for s in image_slots if s.get("position") == slot_key), None
            )
            if matching_slot:
                chart_path = chart_paths.pop(0) if chart_paths else ""
                caption = matching_slot.get("caption", heading)
                styler.add_image(chart_path, caption=caption)

        # ── Tables
        tables = word_struct.get("tables", [])
        if tables:
            styler.add_heading("Data Tables", level=1)
        for tbl in tables:
            styler.add_table(
                headers=tbl.get("headers", []),
                rows=tbl.get("rows", []),
                caption=tbl.get("caption", "")
            )

        # ── Insights
        missing_info = insights.get("missing_info", [])
        if missing_info:
            styler.add_bullet_list(missing_info, label="Areas for Further Investigation")

        suggested = insights.get("suggested_articles", [])
        if suggested:
            styler.add_bullet_list(suggested, label="Suggested Follow-up Documents")

        # ── References (backlinks)
        refs = notion.get("backlinks", []) + notion.get("wikilinks", [])
        if refs:
            styler.add_references(refs)

        # ── Footer
        styler.add_footer_metadata({
            "generated_by": DEFAULT_AUTHOR,
            "date": notion.get("created_at", datetime.now().strftime("%Y-%m-%d")),
            "pe_score": payload.get("pe_score_final", "N/A")
        })

        doc.save(output_path)
        self._log(f"Document saved → {output_path}")
        return output_path

    def from_simple(self, title: str, content: str, output_path: str,
                    tags: list = None, domain: str = "") -> str:
        """Quick mode: generate Word doc from title + plain content string."""
        self._log(f"Quick mode: building '{title}'")
        doc = Document()
        styler = DocumentStyler(doc)

        styler.add_title(title)
        if domain:
            styler.add_heading(f"Domain: {domain.upper()}", level=3)
        styler.add_abstract(content[:300] + "..." if len(content) > 300 else content)
        styler.add_heading("Full Content", level=1)
        styler.add_body(content)

        if tags:
            styler.add_heading("Tags", level=3)
            styler.add_body(" · ".join(tags))

        styler.add_footer_metadata({
            "generated_by": DEFAULT_AUTHOR,
            "date": datetime.now().strftime("%Y-%m-%d")
        })

        doc.save(output_path)
        self._log(f"Document saved → {output_path}")
        return output_path

    def _collect_chart_paths(self, docx_path: str) -> list:
        """Auto-discover chart images in same directory as output docx."""
        base_dir = Path(docx_path).parent / "charts"
        if not base_dir.exists():
            return []
        exts = (".png", ".jpg", ".jpeg")
        return sorted([str(p) for p in base_dir.iterdir() if p.suffix.lower() in exts])


# ─────────────────────────────────────────────────────────
# VALIDATION (PE-3 compatible)
# ─────────────────────────────────────────────────────────
class DocumentValidator:
    """PE-3 style validation for generated Word documents."""

    @staticmethod
    def validate_payload(payload: dict) -> dict:
        errors = []
        warnings = []

        if not payload.get("notion_data", {}).get("title"):
            errors.append("Missing: notion_data.title")
        if not payload.get("word_doc_structure", {}).get("sections"):
            warnings.append("No sections defined in word_doc_structure")
        if not payload.get("notion_data", {}).get("summary"):
            warnings.append("No summary/abstract provided")

        score = 100 - (len(errors) * 20) - (len(warnings) * 5)
        return {
            "errors": errors,
            "warnings": warnings,
            "quality_score": max(0, score),
            "valid": len(errors) == 0
        }


# ─────────────────────────────────────────────────────────
# CLI ENTRY POINT
# ─────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description=f"KM-PIPE DocumentAgent v{VERSION} — Word Document Generator"
    )
    parser.add_argument("--input", "-i", help="Path to KM-PIPE JSON payload file")
    parser.add_argument("--output", "-o", default="output.docx", help="Output .docx path")
    parser.add_argument("--title", "-t", help="Simple mode: document title")
    parser.add_argument("--content", "-c", help="Simple mode: document content")
    parser.add_argument("--domain", "-d", default="", help="Domain tag (semiconductor/ai/etc)")
    parser.add_argument("--tags", nargs="+", default=[], help="Tags list")
    parser.add_argument("--validate-only", action="store_true", help="Validate payload without generating")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress log output")
    args = parser.parse_args()

    generator = WordDocumentGenerator(verbose=not args.quiet)

    if args.input:
        # Full pipeline mode
        with open(args.input, "r", encoding="utf-8") as f:
            payload = json.load(f)

        if args.validate_only:
            result = DocumentValidator.validate_payload(payload)
            print(json.dumps(result, indent=2, ensure_ascii=False))
            sys.exit(0 if result["valid"] else 1)

        out = generator.from_json(payload, args.output)
        print(f"✅ Document generated: {out}")

    elif args.title and args.content:
        # Quick mode
        out = generator.from_simple(
            title=args.title,
            content=args.content,
            output_path=args.output,
            tags=args.tags,
            domain=args.domain
        )
        print(f"✅ Document generated: {out}")

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
