# T-11 PDF Build Guide

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements_pdf.txt

# 2. §C only — quick LP preview (EN)
python convert_to_pdf.py --section-c-only --open

# 3. Full LP package (EN)
python convert_to_pdf.py --lang en --open

# 4. Full LP package (KR)
python convert_to_pdf.py --lang kr

# 5. Encrypted output (LP배포용 AES-256)
python convert_to_pdf.py --lang en --encrypt "T11_OWNER_2026"
```

## Output Location
```
applied-cases/T-11-glass-hbm-investment/06_output/
  T11_LP_Submission_EN_v2.1_<YYYYMMDD>.pdf       ← full package
  T11_LP_Submission_EN_v2.1_SectionC_<DATE>.pdf  ← §C only
```

## File Map

| Script | Role |
|--------|------|
| `cover_page_EN.html` | 다크 테마 표지 (A4, HTML/CSS Paged Media) |
| `convert_to_pdf.py` | 표지 + MD → PDF 변환 + 병합 + 북마크 + 암호화 |
| `requirements_pdf.txt` | pip 의존성 목록 |

## PDF Build Pipeline

```
cover_page_EN.html ──┐
                     ├── WeasyPrint ──► cover.pdf ──┐
T11_section_c_EN.md ─┤                              ├── PyMuPDF merge
                     └── Markdown + WeasyPrint      ├── add_bookmarks()
                              ──► body.pdf ──────────┤
                                                     └──► T11_LP_Submission_EN_v2.1.pdf
```

## Flags Reference

| Flag | Description |
|------|-------------|
| `--lang en\|kr` | Output language |
| `--section-c-only` | §C only (faster) |
| `--no-bookmarks` | Skip TOC injection |
| `--encrypt OWNER_PW` | AES-256 encrypt |
| `--open` | Auto-open in viewer |

## Notes
- WeasyPrint requires system-level fonts (Pango + Cairo). See `requirements_pdf.txt`.
- Korean PDF (`--lang kr`) requires `cover_page_KR.html` (not yet generated).
- LP 배포 전 반드시 `--encrypt` 플래그 사용 권장.
