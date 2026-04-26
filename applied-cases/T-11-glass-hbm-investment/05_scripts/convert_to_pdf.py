#!/usr/bin/env python3
"""
T-11 LP Submission PDF Builder
================================
Converts Markdown report + HTML cover page into a single LP-ready PDF.

Dependencies (install once):
    pip install weasyprint markdown pymupdf
    # OR: pip install weasyprint markdown PyMuPDF

Usage:
    python convert_to_pdf.py                    # default: EN package
    python convert_to_pdf.py --lang kr          # Korean package
    python convert_to_pdf.py --lang en --open   # EN package + auto-open
    python convert_to_pdf.py --section-c-only   # §C only (quick preview)

Output:
    output/T11_LP_Submission_EN_v2.1_<YYYYMMDD>.pdf
    output/T11_LP_Submission_KR_v2.1_<YYYYMMDD>.pdf
"""

import argparse
import os
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

# ── OPTIONAL: rich console for pretty output ──────────────────────────────────
try:
    from rich.console import Console
    from rich.progress import track
    console = Console()
    log = console.print
except ImportError:
    def log(*args, **kwargs): print(*args)
    def track(iterable, **kwargs): return iterable

# ── PATH CONFIGURATION ────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).resolve().parent.parent          # T-11 root
REPORTS    = BASE_DIR / "04_reports"
SCRIPTS    = BASE_DIR / "05_scripts"
OUTPUT     = BASE_DIR / "06_output"
OUTPUT.mkdir(exist_ok=True)

# ── FILE MANIFEST ─────────────────────────────────────────────────────────────
FILES = {
    "en": {
        "cover_html" : SCRIPTS / "cover_page_EN.html",
        "section_c"  : REPORTS / "T11_section_c_enhanced_v2.1_EN.md",
        "main_report": REPORTS / "T11_investment_report_v2.0.md",
        "output_stem": "T11_LP_Submission_EN_v2.1",
    },
    "kr": {
        "cover_html" : SCRIPTS / "cover_page_KR.html",      # future
        "section_c"  : REPORTS / "T11_section_c_enhanced_v2.1.md",
        "main_report": REPORTS / "T11_investment_report_v2.0.md",
        "output_stem": "T11_LP_Submission_KR_v2.1",
    },
}

# ── CSS STYLESHEET (injected into Markdown-converted HTML) ───────────────────
STYLESHEET = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

@page {
  size: A4;
  margin: 22mm 20mm 22mm 20mm;
  @bottom-center {
    content: "CONFIDENTIAL — T-11 Investment Strategy v2.1  |  Page " counter(page) " of " counter(pages);
    font-size: 8pt;
    color: #888;
    font-family: 'Inter', Helvetica, Arial, sans-serif;
  }
  @top-right {
    content: "T-11 Glass/HBM Investment Strategy";
    font-size: 8pt;
    color: #aaa;
    font-family: 'Inter', Helvetica, Arial, sans-serif;
  }
}

body {
  font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
  font-size: 10pt;
  line-height: 1.65;
  color: #1a1a2e;
  background: #ffffff;
}

h1 { font-size: 20pt; color: #0a0f2e; margin-top: 2em; margin-bottom: 0.4em;
     border-bottom: 2px solid #0057ff; padding-bottom: 6px; }
h2 { font-size: 15pt; color: #0a0f2e; margin-top: 1.6em; margin-bottom: 0.3em;
     border-left: 4px solid #00d4ff; padding-left: 10px; }
h3 { font-size: 12pt; color: #1a2a5e; margin-top: 1.3em; }
h4 { font-size: 10pt; color: #2a3a6e; margin-top: 1em; }

p   { margin: 0.5em 0; }

a   { color: #0057ff; text-decoration: none; }

/* Tables */
table {
  border-collapse: collapse;
  width: 100%;
  margin: 1.2em 0;
  font-size: 9pt;
  page-break-inside: avoid;
}
thread { background: #f0f4ff; }
th {
  background: #0a0f2e;
  color: #ffffff;
  padding: 7px 10px;
  text-align: left;
  font-size: 8.5pt;
  letter-spacing: 0.5px;
}
td {
  padding: 7px 10px;
  border-bottom: 1px solid #e0e6f0;
  vertical-align: top;
}
tr:nth-child(even) td { background: #f8f9ff; }

/* Code blocks (term sheet boxes) */
pre, code {
  font-family: 'Courier New', Courier, monospace;
  font-size: 8pt;
  background: #f4f6fb;
  border: 1px solid #dde3f0;
  border-radius: 3px;
  padding: 12px 14px;
  white-space: pre-wrap;
  word-break: break-word;
  color: #1a1a2e;
  page-break-inside: avoid;
}

/* Blockquotes (confidential notice) */
blockquote {
  border-left: 4px solid #ff6b6b;
  background: #fff5f5;
  padding: 10px 16px;
  margin: 1em 0;
  font-size: 9pt;
  color: #c0392b;
}

/* Horizontal rule */
hr { border: none; border-top: 1px solid #dde3f0; margin: 1.5em 0; }

/* Checkmarks in validation table */
td:contains('✅') { color: #16a34a; font-weight: 600; }

/* Page break before major sections */
.page-break { page-break-before: always; }
"""


def check_dependencies() -> bool:
    """Verify required Python packages are installed."""
    missing = []
    for pkg in ("weasyprint", "markdown", "fitz"):   # fitz = pymupdf
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg if pkg != "fitz" else "PyMuPDF")
    if missing:
        log(f"[red]Missing packages: {', '.join(missing)}[/red]")
        log("[yellow]Run: pip install weasyprint markdown PyMuPDF[/yellow]")
        return False
    return True


def md_to_html(md_path: Path, stylesheet: str) -> str:
    """Convert a Markdown file to a full HTML string with embedded CSS."""
    import markdown
    from markdown.extensions import tables, fenced_code, toc

    md_text = md_path.read_text(encoding="utf-8")

    # Strip YAML front-matter (---...---)
    if md_text.startswith("---"):
        end = md_text.find("---", 3)
        if end != -1:
            md_text = md_text[end + 3:].lstrip()

    body_html = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "toc", "nl2br", "sane_lists"],
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <style>{stylesheet}</style>
</head>
<body>
{body_html}
</body>
</html>
"""


def html_to_pdf(html_str: str, out_path: Path) -> None:
    """Render HTML string to a PDF file via WeasyPrint."""
    from weasyprint import HTML, CSS
    HTML(string=html_str).write_pdf(str(out_path))


def merge_pdfs(cover_pdf: Path, body_pdf: Path, final_path: Path) -> None:
    """Merge cover PDF + body PDF into one file using PyMuPDF."""
    import fitz
    doc = fitz.open(str(cover_pdf))
    body = fitz.open(str(body_pdf))
    doc.insert_pdf(body)
    doc.save(str(final_path))
    doc.close()
    body.close()
    log(f"[green]✅ Merged PDF saved: {final_path}[/green]")


def build_section_c_only(lang: str) -> Path:
    """Quick-build: cover + §C only (no full report body)."""
    cfg = FILES[lang]
    date_str = datetime.today().strftime("%Y%m%d")
    final_path = OUTPUT / f"{cfg['output_stem']}_SectionC_{date_str}.pdf"

    log(f"[cyan]Building §C-only PDF ({lang.upper()}) ...[/cyan]")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)

        # 1. Cover
        cover_pdf = tmp / "cover.pdf"
        from weasyprint import HTML
        HTML(filename=str(cfg["cover_html"])).write_pdf(str(cover_pdf))
        log("  [✓] Cover page rendered")

        # 2. §C body
        body_html = md_to_html(cfg["section_c"], STYLESHEET)
        body_pdf  = tmp / "body.pdf"
        html_to_pdf(body_html, body_pdf)
        log("  [✓] §C body rendered")

        # 3. Merge
        merge_pdfs(cover_pdf, body_pdf, final_path)

    return final_path


def build_full_package(lang: str) -> Path:
    """Full build: cover + main report (§A–§B, §D–§F) + §C replacement."""
    cfg = FILES[lang]
    date_str = datetime.today().strftime("%Y%m%d")
    final_path = OUTPUT / f"{cfg['output_stem']}_{date_str}.pdf"

    log(f"[cyan]Building full LP package ({lang.upper()}) ...[/cyan]")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)

        # 1. Cover
        cover_pdf = tmp / "cover.pdf"
        from weasyprint import HTML
        HTML(filename=str(cfg["cover_html"])).write_pdf(str(cover_pdf))
        log("  [✓] Cover page rendered")

        # 2. Main report body (§A–§F minus §C)
        body_html   = md_to_html(cfg["main_report"], STYLESHEET)
        body_pdf    = tmp / "body.pdf"
        html_to_pdf(body_html, body_pdf)
        log("  [✓] Main report rendered")

        # 3. §C replacement
        sec_c_html  = md_to_html(cfg["section_c"], STYLESHEET)
        sec_c_pdf   = tmp / "sec_c.pdf"
        html_to_pdf(sec_c_html, sec_c_pdf)
        log("  [✓] §C replacement rendered")

        # 4. Merge: cover + body + §C
        import fitz
        doc = fitz.open(str(cover_pdf))
        for part in (body_pdf, sec_c_pdf):
            doc.insert_pdf(fitz.open(str(part)))
        doc.save(str(final_path))
        doc.close()
        log(f"[green]✅ Full LP package saved: {final_path}[/green]")

    return final_path


def add_bookmarks(pdf_path: Path) -> None:
    """
    Post-process: inject PDF bookmarks (TOC) for LP navigation.
    Sections are inferred from heading text in the PDF.
    """
    import fitz
    doc = fitz.open(str(pdf_path))
    toc = [
        [1, "Cover Page",                    1],
        [1, "§C — Investment Execution Model", 2],
        [2, "C.1  Executive Summary",          2],
        [2, "C.2  Term Sheets",                3],
        [3, "C.2.1  Type A — Glass JV",        3],
        [3, "C.2.2  Type B — HBM Offtake",     4],
        [3, "C.2.3  Type C — Amkor / Micron CB",5],
        [2, "C.3  Due Diligence Framework",    6],
        [2, "C.4  IC Memorandum",              7],
        [2, "C.5  Exit Structure",             8],
        [2, "C.6  Monitoring KPIs",            9],
        [2, "C.7  Execution Timeline",         10],
        [2, "C.8  Validation Gate",            11],
    ]
    doc.set_toc(toc)
    doc.save(str(pdf_path), incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
    doc.close()
    log("  [✓] PDF bookmarks (TOC) injected")


def encrypt_pdf(pdf_path: Path, owner_pw: str, user_pw: str = "") -> None:
    """
    Optional: encrypt PDF with owner/user passwords.
    Owner password required to modify; user password required to open.
    """
    import fitz
    doc   = fitz.open(str(pdf_path))
    perm  = (
        fitz.PDF_PERM_PRINT          # allow printing
        | fitz.PDF_PERM_COPY         # allow copy (required for screen-reader)
    )                                # no editing, no extraction
    doc.save(
        str(pdf_path),
        encryption=fitz.PDF_ENCRYPT_AES_256,
        owner_pw=owner_pw,
        user_pw=user_pw,
        permissions=perm,
    )
    doc.close()
    log("  [✓] PDF encrypted (AES-256)")


def open_pdf(pdf_path: Path) -> None:
    """Open generated PDF in the system default viewer."""
    if sys.platform == "win32":
        os.startfile(str(pdf_path))
    elif sys.platform == "darwin":
        subprocess.run(["open", str(pdf_path)])
    else:
        subprocess.run(["xdg-open", str(pdf_path)])


# ── CLI ────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="T-11 LP Submission PDF Builder"
    )
    parser.add_argument(
        "--lang", choices=["en", "kr"], default="en",
        help="Output language (default: en)"
    )
    parser.add_argument(
        "--section-c-only", action="store_true",
        help="Build §C-only PDF (faster, for quick review)"
    )
    parser.add_argument(
        "--no-bookmarks", action="store_true",
        help="Skip PDF bookmark injection"
    )
    parser.add_argument(
        "--encrypt", metavar="OWNER_PW",
        help="Encrypt PDF with owner password (AES-256)"
    )
    parser.add_argument(
        "--open", action="store_true",
        help="Open PDF in system viewer after build"
    )
    args = parser.parse_args()

    log("[bold blue]T-11 PDF Builder[/bold blue] — LP Submission Package")
    log(f"  Language : {args.lang.upper()}")
    log(f"  Date     : {datetime.today().strftime('%Y-%m-%d %H:%M')}")
    log("")

    if not check_dependencies():
        sys.exit(1)

    # ── BUILD ──────────────────────────────────────────────────────────────────
    if args.section_c_only:
        pdf_path = build_section_c_only(args.lang)
    else:
        pdf_path = build_full_package(args.lang)

    # ── POST-PROCESS ───────────────────────────────────────────────────────────
    if not args.no_bookmarks:
        add_bookmarks(pdf_path)

    if args.encrypt:
        encrypt_pdf(pdf_path, owner_pw=args.encrypt, user_pw="")

    # ── SUMMARY ────────────────────────────────────────────────────────────────
    size_kb = pdf_path.stat().st_size // 1024
    log("")
    log(f"[bold green]Build complete![/bold green]")
    log(f"  Output : {pdf_path}")
    log(f"  Size   : {size_kb:,} KB")
    log("")
    log("LP distribution checklist:")
    log("  □ Verify all figures match KR v2.1 source")
    log("  □ Confirm watermark / confidentiality notice visible")
    log("  □ Test PDF bookmarks in Acrobat / Preview")
    log("  □ Share via secure channel only (no public links)")

    if args.open:
        open_pdf(pdf_path)


if __name__ == "__main__":
    main()
