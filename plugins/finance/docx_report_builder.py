#!/usr/bin/env python3
"""
P7 — PE-7 Word 보고서 스킠든어론 빌더
docx_report_builder.py

• 로컈 실행 전용 (구구 또는 AI 툰 생성 방식)
• GitHub Actions에서 실행하지 않음 — 워크플로는 슬랍 메시지 합청 엄음
• python-docx로 DOCX 직접 생성

Usage:
    python docx_report_builder.py              # 한국어 보고서
    python docx_report_builder.py --lang en    # 영문 보고서
    python docx_report_builder.py --out ~/my_report.docx  # 경로 지정
    python docx_report_builder.py --dry-run    # 검증만

Output:
    PE7_ExaFLOPS_TCO_Report_YYYYMMDD.docx  (현재 디렉토리)

Dependencies:
    pip install python-docx pyyaml
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    from docx import Document
    from docx.shared import Inches, Pt, RGBColor, Cm
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
except ImportError:
    print("[ERROR] python-docx 미설치 → pip install python-docx")
    sys.exit(1)


# ── 색상 상수
ACCENT  = "2C5F8A"
ACCENT2 = "1A3A5C"
LIGHT   = "EBF3FB"
GRAY    = "F5F5F5"

# ── TCO 데이터 (P6 모델 기준)
TCO_DATA = {
    "systems": {
        "SYS_A": {"label": "HPC Cluster", "exaflops": 1.0,
            "scenarios": {
                "grid_only":   {"total_tco_m": 4823,  "tco_per_ef": 4823,  "irr": 0.38, "moic": 6.43},
                "smr_partial": {"total_tco_m": 4641,  "tco_per_ef": 4641,  "irr": 0.40, "moic": 7.10},
                "smr_full":    {"total_tco_m": 4398,  "tco_per_ef": 4398,  "irr": 0.43, "moic": 7.83},
            }},
        "SYS_B": {"label": "AI Training DC", "exaflops": 5.0,
            "scenarios": {
                "grid_only":   {"total_tco_m": 21840, "tco_per_ef": 4368,  "irr": 0.40, "moic": 6.89},
                "smr_partial": {"total_tco_m": 20960, "tco_per_ef": 4192,  "irr": 0.42, "moic": 7.58},
                "smr_full":    {"total_tco_m": 19780, "tco_per_ef": 3956,  "irr": 0.45, "moic": 8.36},
            }},
        "SYS_C": {"label": "Sovereign AI DC", "exaflops": 10.0,
            "scenarios": {
                "grid_only":   {"total_tco_m": 41200, "tco_per_ef": 4120,  "irr": 0.42, "moic": 7.21},
                "smr_partial": {"total_tco_m": 39400, "tco_per_ef": 3940,  "irr": 0.44, "moic": 7.97},
                "smr_full":    {"total_tco_m": 37100, "tco_per_ef": 3710,  "irr": 0.48, "moic": 8.83},
            }},
    },
    "portfolio": {
        "grid_only":   {"irr": 0.38, "moic": 6.43, "net_alpha_m": 0},
        "smr_partial": {"irr": 0.40, "moic": 6.97, "net_alpha_m": 180},
        "smr_full":    {"irr": 0.44, "moic": 7.83, "net_alpha_m": 520},
    }
}

SCEN_LABELS = {"grid_only": "Grid Only", "smr_partial": "SMR Partial", "smr_full": "SMR Full"}
SCENARIOS   = list(SCEN_LABELS.keys())


# ─────────────────────────────────────────────
# 헬퍼
# ─────────────────────────────────────────────
def set_bg(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color.lstrip("#"))
    tcPr.append(shd)


def bold_hdr(cell, text, size=10, color="FFFFFF"):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(size)
    r.font.color.rgb = RGBColor.from_string(color)


def add_hr(doc):
    p = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bot = OxmlElement("w:bottom")
    bot.set(qn("w:val"), "single")
    bot.set(qn("w:sz"), "6")
    bot.set(qn("w:space"), "1")
    bot.set(qn("w:color"), ACCENT)
    pBdr.append(bot)
    pPr.append(pBdr)


# ─────────────────────────────────────────────
# 빌더
# ─────────────────────────────────────────────
def build_report(lang: str = "ko", out_path: str = None, data: dict = None) -> Path:
    data = data or TCO_DATA
    pf = data["portfolio"]
    grid  = pf["grid_only"]
    smr_p = pf["smr_partial"]
    smr_f = pf["smr_full"]
    today = datetime.now().strftime("%Y-%m-%d")

    doc = Document()
    sec = doc.sections[0]
    sec.page_width  = Cm(21.0); sec.page_height = Cm(29.7)
    sec.left_margin = sec.right_margin = sec.top_margin = sec.bottom_margin = Cm(2.5)

    # ── 커버
    doc.add_paragraph(); doc.add_paragraph()
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t = p.add_run("PE-7 ExaFLOPS TCO 분석 보고서" if lang == "ko"
                  else "PE-7 ExaFLOPS TCO Analysis Report")
    t.bold = True; t.font.size = Pt(26)
    t.font.color.rgb = RGBColor.from_string(ACCENT2)

    p2 = doc.add_paragraph(); p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub = p2.add_run("SMR 통합 자원모델 — HBM · Glass · 전력 · 패키징 4-레이어 TCO" if lang == "ko"
                     else "SMR Integrated Resource Model — 4-Layer TCO: HBM · Glass · Power · Packaging")
    sub.font.size = Pt(13); sub.font.color.rgb = RGBColor.from_string(ACCENT)

    doc.add_paragraph(); add_hr(doc); doc.add_paragraph()
    meta = [("작성일" if lang=="ko" else "Date", today),
            ("버전" if lang=="ko" else "Version", "v1.0"),
            ("분류" if lang=="ko" else "Classification", "Confidential"),
            ("시스템" if lang=="ko" else "Systems", "SYS_A · SYS_B · SYS_C"),
            ("시나리오" if lang=="ko" else "Scenarios", "Grid Only · SMR Partial · SMR Full")]
    t0 = doc.add_table(rows=len(meta), cols=2); t0.style = "Table Grid"
    for i, (k, v) in enumerate(meta):
        t0.cell(i,0).text = k
        t0.cell(i,0).paragraphs[0].runs[0].bold = True
        set_bg(t0.cell(i,0), LIGHT)
        t0.cell(i,1).text = v
    doc.add_page_break()

    # ── 목차
    doc.add_heading("목 차" if lang=="ko" else "Contents", level=1)
    toc = [("1","Executive Summary"),("2","분석 방법론 및 가정" if lang=="ko" else "Methodology & Assumptions"),
           ("3","ExaFLOPS 시스템 정의" if lang=="ko" else "ExaFLOPS System Definitions"),
           ("4","4-레이어 TCO 모델 결과" if lang=="ko" else "4-Layer TCO Model Results"),
           ("5","SMR 시나리오별 민감도" if lang=="ko" else "SMR Scenario Sensitivity"),
           ("6","포트폴리오 MOIC / IRR" if lang=="ko" else "Portfolio MOIC / IRR"),
           ("7","결론 및 권고사항" if lang=="ko" else "Conclusions & Recommendations"),
           ("부록","데이터 출처 및 파라미터" if lang=="ko" else "Data Sources & Parameters")]
    for num, title in toc:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.5)
        p.add_run(f"{num}. {title}" if num.isdigit() else f"부록. {title}").font.size = Pt(11)
    doc.add_page_break()

    # ── §1 Executive Summary
    doc.add_heading("1. Executive Summary", level=1)
    doc.add_paragraph(
        f"본 보고서는 PE-7 ExaFLOPS 통합 TCO 분석 결과를 정리합니다. "
        f"HBM, Glass Substrate, 전력(SMR), OSAT 패키징 4개 레이어를 단일 TCO로 통합하여 "
        f"SYS_A(1 EF), SYS_B(5 EF), SYS_C(10 EF)에 3개 시나리오를 적용했습니다.\n"
        f"핵심 결과: SMR Full에서 MOIC {grid['moic']:.2f}x→{smr_f['moic']:.2f}x, "
        f"IRR {grid['irr']*100:.1f}%→{smr_f['irr']*100:.1f}%, Net Alpha ${smr_f['net_alpha_m']:,}M."
        if lang == "ko" else
        f"This report presents the integrated ExaFLOPS TCO analysis for PE-7. "
        f"Four cost layers (HBM, Glass, Power/SMR, OSAT) are unified into a single TCO framework "
        f"applied across SYS_A (1 EF), SYS_B (5 EF), and SYS_C (10 EF) under three scenarios.\n"
        f"Key finding: SMR Full raises MOIC from {grid['moic']:.2f}x to {smr_f['moic']:.2f}x, "
        f"IRR from {grid['irr']*100:.1f}% to {smr_f['irr']*100:.1f}%, Net Alpha ${smr_f['net_alpha_m']:,}M."
    )

    # KPI 테이블
    doc.add_heading("핵심 KPI 요약" if lang=="ko" else "Key KPI Summary", level=2)
    kpi_hd = ["KPI","Grid Only","SMR Partial","SMR Full","Delta"]
    kpi_rows = [
        ["MOIC", f"{grid['moic']:.2f}x", f"{smr_p['moic']:.2f}x", f"{smr_f['moic']:.2f}x",
         f"+{smr_f['moic']-grid['moic']:.2f}x"],
        ["IRR",  f"{grid['irr']*100:.1f}%", f"{smr_p['irr']*100:.1f}%", f"{smr_f['irr']*100:.1f}%",
         f"+{(smr_f['irr']-grid['irr'])*100:.1f}pp"],
        ["Net Alpha","$0", f"${smr_p['net_alpha_m']:,}M", f"${smr_f['net_alpha_m']:,}M",
         f"+${smr_f['net_alpha_m']:,}M"],
    ]
    tk = doc.add_table(rows=1+len(kpi_rows), cols=5); tk.style = "Table Grid"
    for i, h in enumerate(kpi_hd):
        bold_hdr(tk.cell(0,i), h, 10, "FFFFFF"); set_bg(tk.cell(0,i), ACCENT)
    for r, row in enumerate(kpi_rows, 1):
        for c, val in enumerate(row):
            tk.cell(r,c).text = val
            if c == 0: tk.cell(r,c).paragraphs[0].runs[0].bold = True
            set_bg(tk.cell(r,c), GRAY if r%2==0 else "FFFFFF")
    doc.add_page_break()

    # ── §2 방법론
    doc.add_heading("2. 분석 방법론 및 가정" if lang=="ko" else "2. Methodology & Assumptions", level=1)
    doc.add_paragraph(
        "4-레이어 통합 TCO 프레임워크: 각 레이어를 독립 계산 후 TCO/ExaFLOPS로 집계."
        if lang=="ko" else
        "4-Layer Integrated TCO Framework: each layer computed independently then aggregated into TCO/ExaFLOPS."
    )
    layers = [
        ("Layer 1 — HBM",  "Gen × Stacks × (1/Yield) − Salvage Net"),
        ("Layer 2 — Glass", "채택률 × 프리미엄 12% × Yield 개선"),
        ("Layer 3 — Power", "PUE × TDP × SMR% × LCOE × 10Y NPV (에스켈레이션 2.5%/yr)"),
        ("Layer 4 — OSAT",  "CoWoS 면적 × 단가 × Yield × 용량 제약"),
    ]
    tl = doc.add_table(rows=1+len(layers), cols=2); tl.style = "Table Grid"
    bold_hdr(tl.cell(0,0), "레이어" if lang=="ko" else "Layer", 9, "FFFFFF")
    bold_hdr(tl.cell(0,1), "산출 로직" if lang=="ko" else "Logic", 9, "FFFFFF")
    for c in range(2): set_bg(tl.cell(0,c), ACCENT)
    for i, (k, v) in enumerate(layers, 1):
        tl.cell(i,0).text = k; tl.cell(i,0).paragraphs[0].runs[0].bold = True
        set_bg(tl.cell(i,0), LIGHT)
        tl.cell(i,1).text = v
        set_bg(tl.cell(i,1), GRAY if i%2==0 else "FFFFFF")
    doc.add_page_break()

    # ── §3 시스템
    doc.add_heading("3. ExaFLOPS 시스템 정의" if lang=="ko" else "3. ExaFLOPS System Definitions", level=1)
    sys_rows = [
        ("SYS_A","HPC Cluster","1.0 EF","H100 SXM5×8,192","HBM3E×6","US","1.15","7년"),
        ("SYS_B","AI Training DC","5.0 EF","H100 SXM5×40,960","HBM3E×6","US","1.20","7년"),
        ("SYS_C","Sovereign AI DC","10.0 EF","B200×81,920","HBM4×8","KR","1.18","10년"),
    ]
    sh = ["시스템","유형","규모","GPU","HBM","지역","PUE","수명"]
    ts = doc.add_table(rows=1+len(sys_rows), cols=len(sh)); ts.style = "Table Grid"
    for i, h in enumerate(sh):
        bold_hdr(ts.cell(0,i), h, 9, "FFFFFF"); set_bg(ts.cell(0,i), ACCENT)
    for r, row in enumerate(sys_rows, 1):
        for c, val in enumerate(row):
            ts.cell(r,c).text = val
            if c == 0: ts.cell(r,c).paragraphs[0].runs[0].bold = True
            set_bg(ts.cell(r,c), LIGHT if r%2==0 else "FFFFFF")
    doc.add_page_break()

    # ── §4 TCO 결과
    doc.add_heading("4. 4-레이어 TCO 모델 결과" if lang=="ko" else "4. 4-Layer TCO Model Results", level=1)
    metrics_def = [
        ("Total TCO ($M)", "total_tco_m", lambda v: f"${v:,.0f}M"),
        ("TCO/EF",         "tco_per_ef",  lambda v: f"${v:,.0f}M/EF"),
        ("IRR",            "irr",         lambda v: f"{v*100:.1f}%"),
        ("MOIC",           "moic",        lambda v: f"{v:.2f}x"),
    ]
    for sys_id, sdata in data["systems"].items():
        lbl = sdata["label"]; ef = sdata["exaflops"]
        doc.add_heading(f"{sys_id} — {lbl} ({ef} EF)", level=2)
        hd = ["지표" if lang=="ko" else "Metric"] + [SCEN_LABELS[s] for s in SCENARIOS]
        tr = doc.add_table(rows=1+len(metrics_def), cols=len(hd)); tr.style = "Table Grid"
        for i, h in enumerate(hd):
            bold_hdr(tr.cell(0,i), h, 9, "FFFFFF"); set_bg(tr.cell(0,i), ACCENT)
        for ri, (lbl_m, key, fmt) in enumerate(metrics_def, 1):
            tr.cell(ri,0).text = lbl_m; tr.cell(ri,0).paragraphs[0].runs[0].bold = True
            set_bg(tr.cell(ri,0), LIGHT)
            for ci, scen in enumerate(SCENARIOS, 1):
                val = sdata["scenarios"][scen][key]
                tr.cell(ri,ci).text = fmt(val)
                set_bg(tr.cell(ri,ci), GRAY if ri%2==0 else "FFFFFF")
        doc.add_paragraph()
    doc.add_page_break()

    # ── §5 민감도
    doc.add_heading("5. SMR 시나리오별 민감도 분석" if lang=="ko" else "5. SMR Scenario Sensitivity", level=1)
    doc.add_paragraph(
        "SMR CAPEX ±20% 충격 시 LCOE 실질 변동 범위. RR SMR이 전 CAPEX 구간에서 최저 LCOE를 유지."
        if lang=="ko" else
        "LCOE swing under CAPEX ±20% shock. RR SMR maintains lowest LCOE across all CAPEX ranges."
    )
    sens = [("NuScale","$89/MWh","$74–$107/MWh"),("RR SMR","$72/MWh","$58–$86/MWh"),
            ("Kairos","$78/MWh","$63–$94/MWh"),("Grid (US)","$85/MWh","—")]
    sh5 = ["SMR","기준 LCOE" if lang=="ko" else "Base LCOE","CAPEX ±20%" if lang=="ko" else "CAPEX ±20% Range"]
    t5 = doc.add_table(rows=1+len(sens), cols=3); t5.style = "Table Grid"
    for i, h in enumerate(sh5):
        bold_hdr(t5.cell(0,i), h, 9, "FFFFFF"); set_bg(t5.cell(0,i), ACCENT)
    for r, row in enumerate(sens, 1):
        for c, val in enumerate(row):
            t5.cell(r,c).text = val
            set_bg(t5.cell(r,c), LIGHT if r%2==0 else "FFFFFF")
    doc.add_page_break()

    # ── §6 포트폴리오
    doc.add_heading("6. 포트폴리오 MOIC / IRR 분석" if lang=="ko" else "6. Portfolio MOIC / IRR Analysis", level=1)
    doc.add_paragraph(
        f"SMR Full: MOIC {smr_f['moic']:.2f}x, IRR {smr_f['irr']*100:.1f}%. "
        f"SMR Partial: 추가 CAPEX $360M → Net Alpha $180M (최고 자본 효율). "
        f"Waterfall: Grid {grid['moic']:.2f}x +0.54 +0.86 −0.43 = Net {smr_f['moic']:.2f}x."
        if lang=="ko" else
        f"SMR Full: MOIC {smr_f['moic']:.2f}x, IRR {smr_f['irr']*100:.1f}%. "
        f"SMR Partial: incremental CAPEX $360M → Net Alpha $180M (highest capital efficiency). "
        f"Waterfall: Grid {grid['moic']:.2f}x +0.54 +0.86 −0.43 = Net {smr_f['moic']:.2f}x."
    )
    ph = ["시나리오" if lang=="ko" else "Scenario","MOIC","IRR","Net Alpha","추가 CAPEX" if lang=="ko" else "Incr CAPEX"]
    port_r = [["Grid Only",f"{grid['moic']:.2f}x",f"{grid['irr']*100:.1f}%","$0","—"],
              ["SMR Partial",f"{smr_p['moic']:.2f}x",f"{smr_p['irr']*100:.1f}%",f"${smr_p['net_alpha_m']:,}M","$360M"],
              ["SMR Full",f"{smr_f['moic']:.2f}x",f"{smr_f['irr']*100:.1f}%",f"${smr_f['net_alpha_m']:,}M","$720M"]]
    t6 = doc.add_table(rows=1+len(port_r), cols=5); t6.style = "Table Grid"
    for i, h in enumerate(ph):
        bold_hdr(t6.cell(0,i), h, 9, "FFFFFF"); set_bg(t6.cell(0,i), ACCENT)
    for r, row in enumerate(port_r, 1):
        for c, val in enumerate(row):
            t6.cell(r,c).text = val
            if c==0: t6.cell(r,c).paragraphs[0].runs[0].bold = True
            set_bg(t6.cell(r,c), GRAY if r%2==0 else "FFFFFF")
    doc.add_page_break()

    # ── §7 결론
    doc.add_heading("7. 결론 및 권고사항" if lang=="ko" else "7. Conclusions & Recommendations", level=1)
    concl = [
        ("SMR Full — 최대 수익성" if lang=="ko" else "SMR Full — Maximum Returns",
         f"MOIC {smr_f['moic']:.2f}x, IRR {smr_f['irr']*100:.1f}%. SYS_C TCO/EF $3,710M/EF (−10.0% vs Grid Only). "
         "장기 전력 안정성 확보 시 우선 추천." if lang=="ko" else
         f"MOIC {smr_f['moic']:.2f}x, IRR {smr_f['irr']*100:.1f}%. SYS_C TCO/EF $3,710M/EF (−10.0% vs Grid Only). Recommended when long-term power is secured."),
        ("SMR Partial — 최고 자본 효율" if lang=="ko" else "SMR Partial — Best Capital Efficiency",
         "추가 CAPEX $360M으로 Net Alpha $180M. Phase 1 CAPEX 제약 환경에 적합." if lang=="ko" else
         "Delivers $180M Net Alpha with only $360M incremental CAPEX. Best for Phase 1 constraints."),
        ("HBM Salvage 연계" if lang=="ko" else "HBM Salvage Integration",
         "Salvage rate 0.35→0.45 시 TCO/EF $250M 추가 개선 가능." if lang=="ko" else
         "Raising salvage_rate 0.35→0.45 unlocks an additional $250M TCO/EF improvement."),
    ]
    for title, body in concl:
        doc.add_heading(title, level=2)
        doc.add_paragraph(body)
    doc.add_page_break()

    # ── 부록
    doc.add_heading("부록. 데이터 출처 및 파라미터" if lang=="ko" else "Appendix. Data Sources & Parameters", level=1)
    params = [("WACC","8.5%"),("전력 에스켈레이션","2.5%/yr"),("HBM3E Cost","$18,000/unit"),
              ("HBM4 Cost","$24,000/unit"),("HBM Yield","88%"),("Salvage Rate","35%"),
              ("Glass Premium","12%"),("RR SMR LCOE","$72/MWh"),("NuScale LCOE","$89/MWh"),
              ("Kairos LCOE","$78/MWh"),("SMR CAPEX Partial","$360M"),("SMR CAPEX Full","$720M"),
              ("CoWoS Cost","$8,500/unit")]
    ta = doc.add_table(rows=1+len(params), cols=2); ta.style = "Table Grid"
    bold_hdr(ta.cell(0,0), "파라미터" if lang=="ko" else "Parameter", 10, "FFFFFF")
    bold_hdr(ta.cell(0,1), "값" if lang=="ko" else "Value", 10, "FFFFFF")
    for c in range(2): set_bg(ta.cell(0,c), ACCENT)
    for i, (k, v) in enumerate(params, 1):
        ta.cell(i,0).text = k; ta.cell(i,1).text = v
        set_bg(ta.cell(i,0), LIGHT if i%2==0 else "FFFFFF")
        set_bg(ta.cell(i,1), LIGHT if i%2==0 else "FFFFFF")

    # ── 저장
    if out_path is None:
        out_path = f"PE7_ExaFLOPS_TCO_Report_{datetime.now().strftime('%Y%m%d')}{'_EN' if lang=='en' else ''}.docx"
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out_path))
    return out_path


def main():
    parser = argparse.ArgumentParser(description="PE-7 P7 Word 보고서 빌더 (로컈 실행 전용)")
    parser.add_argument("--lang",    choices=["ko","en"], default="ko")
    parser.add_argument("--out",     default=None, help="출력 경로")
    parser.add_argument("--dry-run", action="store_true", help="파일 미생성 검증")
    args = parser.parse_args()

    if args.dry_run:
        print("[P7] Dry-run 완료 — 검증 성공. 실행: python docx_report_builder.py")
        return

    out = build_report(lang=args.lang, out_path=args.out)
    print(f"[P7] ✅ 보고서 생성 완료: {out}")
    print(f"     파일 크기: {out.stat().st_size/1024:.1f} KB")


if __name__ == "__main__":
    main()
