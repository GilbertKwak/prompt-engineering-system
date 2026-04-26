#!/usr/bin/env python3
"""
P6: ExaFLOPS TCO 시각화 — 5개 차트 자동 생성

차트 목록:
  1. tco_stacked_bar    — 시스템 × 시나리오별 TCO 스택 바 (CAPEX/OPEX 분해)
  2. cost_per_exaflops  — ExaFLOPS당 TCO 비교 (그룹 바)
  3. layer_breakdown    — 4개 자원 레이어별 비용 비중 (파이 × 3)
  4. smr_saving_scatter — SMR 절감액 vs 총 TCO 산점도
  5. glass_adoption_line — Glass 채택률별 Substrate 비용 추이

Usage:
    python exaflops_viz.py
    python exaflops_viz.py --json p6_exaflops_tco.json --out output/p6_charts
"""

import argparse
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ────────────────────────────────────────
# 공통 테마
# ────────────────────────────────────────
COLORS = {
    "capex_hbm":    "#6366f1",
    "capex_glass":  "#8b5cf6",
    "capex_power":  "#06b6d4",
    "capex_other":  "#64748b",
    "opex_power":   "#f59e0b",
    "opex_maint":   "#10b981",
    "opex_other":   "#94a3b8",
    "grid_only":    "#ef4444",
    "smr_partial":  "#f59e0b",
    "smr_full":     "#10b981",
}
SCENARIO_LABELS = {
    "grid_only":   "Grid Only",
    "smr_partial": "SMR 40%",
    "smr_full":    "SMR 80%",
}
SYSTEM_LABELS = {
    "SYS_A": "HPC 1 EF",
    "SYS_B": "AI DC 5 EF",
    "SYS_C": "Sovereign 10 EF",
}

LAYOUT_BASE = dict(
    font=dict(family="Inter, Arial", size=13),
    paper_bgcolor="#ffffff",
    plot_bgcolor="#f8fafc",
    margin=dict(l=60, r=40, t=100, b=60),
    width=1100,
    height=620,
)


def save_chart(fig, name: str, out_dir: str, caption: str, description: str = ""):
    import json as _json
    os.makedirs(out_dir, exist_ok=True)
    png_path  = os.path.join(out_dir, f"{name}.png")
    meta_path = png_path + ".meta.json"
    fig.write_image(png_path)
    with open(meta_path, "w") as f:
        _json.dump({"caption": caption, "description": description}, f)
    print(f"  ✓ {png_path}")
    return png_path


# ────────────────────────────────────────
# 차트 1: TCO 스택 바 (CAPEX/OPEX 분해)
# ────────────────────────────────────────
def chart_tco_stacked(df: pd.DataFrame, out_dir: str):
    base = df[df["Glass Scenario"] == "base"].copy()
    base["label"] = base["System ID"].map(SYSTEM_LABELS) + "<br>" + base["SMR Scenario"].map(SCENARIO_LABELS)

    fig = go.Figure()
    layers = [
        ("CAPEX HBM ($M)",        "HBM",         COLORS["capex_hbm"]),
        ("CAPEX Glass/Pkg ($M)",   "Glass/Pkg",   COLORS["capex_glass"]),
        ("CAPEX Power Infra ($M)", "Power Infra", COLORS["capex_power"]),
        ("CAPEX GPU/Other ($M)",   "GPU/Other",   COLORS["capex_other"]),
        ("OPEX Power ($M)",        "OPEX Power",  COLORS["opex_power"]),
        ("OPEX Maintenance ($M)",  "OPEX Maint",  COLORS["opex_maint"]),
        ("OPEX Other ($M)",        "OPEX Other",  COLORS["opex_other"]),
    ]
    for col, name, color in layers:
        fig.add_trace(go.Bar(
            name=name,
            x=base["label"],
            y=base[col],
            marker_color=color,
            hovertemplate=f"<b>{name}</b>: $%{{y:,.0f}}M<extra></extra>",
        ))

    fig.update_layout(
        **LAYOUT_BASE,
        barmode="stack",
        title=dict(
            text="ExaFLOPS TCO by Layer — CAPEX & OPEX Stack<br>"
                 "<span style='font-size:14px;font-weight:normal'>Source: P6 Model | Lifetime NPV ($M)</span>",
            x=0.5, xanchor="center",
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    )
    fig.update_xaxes(title_text="System × Scenario", tickangle=-30)
    fig.update_yaxes(title_text="TCO ($M)")
    return save_chart(fig, "p6_tco_stacked", out_dir,
                      "ExaFLOPS TCO: CAPEX/OPEX 스택 분해 (P6)",
                      "시스템 × SMR 시나리오별 TCO 구성 레이어 스택 바")


# ────────────────────────────────────────
# 차트 2: ExaFLOPS당 TCO 비교
# ────────────────────────────────────────
def chart_cost_per_exaflops(df: pd.DataFrame, out_dir: str):
    base = df[df["Glass Scenario"] == "base"].copy()
    fig = go.Figure()
    for smr, label in SCENARIO_LABELS.items():
        sub = base[base["SMR Scenario"] == smr]
        fig.add_trace(go.Bar(
            name=label,
            x=[SYSTEM_LABELS.get(s, s) for s in sub["System ID"]],
            y=sub["TCO/ExaFLOPS ($M)"],
            marker_color=COLORS[smr],
            text=sub["TCO/ExaFLOPS ($M)"].apply(lambda v: f"${v:,.0f}M"),
            textposition="outside",
            hovertemplate=f"<b>{label}</b>: $%{{y:,.0f}}M/EF<extra></extra>",
        ))
    fig.update_layout(
        **LAYOUT_BASE,
        barmode="group",
        title=dict(
            text="TCO per ExaFLOPS — SMR Scenario Comparison<br>"
                 "<span style='font-size:14px;font-weight:normal'>Source: P6 Model | Lower is better</span>",
            x=0.5, xanchor="center",
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
    )
    fig.update_xaxes(title_text="System")
    fig.update_yaxes(title_text="$/ExaFLOPS ($M)")
    fig.update_traces(cliponaxis=False)
    return save_chart(fig, "p6_cost_per_exaflops", out_dir,
                      "ExaFLOPS당 TCO: SMR 시나리오 비교 (P6)",
                      "SMR 시나리오별 ExaFLOPS당 단위 비용 그룹 바")


# ────────────────────────────────────────
# 차트 3: 자원 레이어 비중 파이 차트
# ────────────────────────────────────────
def chart_layer_breakdown(df: pd.DataFrame, out_dir: str):
    systems = ["SYS_A", "SYS_B", "SYS_C"]
    fig = make_subplots(
        rows=1, cols=3,
        specs=[[{"type": "domain"}, {"type": "domain"}, {"type": "domain"}]],
        subplot_titles=[SYSTEM_LABELS[s] for s in systems],
    )
    layer_cols = [
        "CAPEX HBM ($M)", "CAPEX Glass/Pkg ($M)",
        "CAPEX Power Infra ($M)", "CAPEX GPU/Other ($M)",
        "OPEX Power ($M)", "OPEX Maintenance ($M)", "OPEX Other ($M)",
    ]
    layer_names = ["HBM", "Glass/Pkg", "Power Infra", "GPU/Other",
                   "OPEX Power", "OPEX Maint", "OPEX Other"]
    layer_colors = [COLORS[k] for k in [
        "capex_hbm", "capex_glass", "capex_power", "capex_other",
        "opex_power", "opex_maint", "opex_other"
    ]]

    for i, sys_id in enumerate(systems, 1):
        sub = df[(df["System ID"] == sys_id) & (df["SMR Scenario"] == "smr_full") & (df["Glass Scenario"] == "base")]
        if sub.empty:
            continue
        vals = [sub[c].values[0] for c in layer_cols]
        fig.add_trace(go.Pie(
            labels=layer_names,
            values=vals,
            marker_colors=layer_colors,
            textinfo="percent",
            hovertemplate="<b>%{label}</b>: $%{value:,.0f}M (%{percent})<extra></extra>",
            showlegend=(i == 1),
        ), row=1, col=i)

    fig.update_layout(
        **{**LAYOUT_BASE, "height": 500},
        title=dict(
            text="TCO Layer Breakdown by System (SMR Full Scenario)<br>"
                 "<span style='font-size:14px;font-weight:normal'>Source: P6 Model | 자원 레이어 비중</span>",
            x=0.5, xanchor="center",
        ),
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="right", x=1.12),
        uniformtext_minsize=11,
        uniformtext_mode="hide",
    )
    return save_chart(fig, "p6_layer_breakdown", out_dir,
                      "시스템별 TCO 레이어 비중 파이차트 (SMR Full)",
                      "3개 시스템 × 7개 자원 레이어 비용 비중")


# ────────────────────────────────────────
# 차트 4: SMR 절감액 vs 총 TCO 산점도
# ────────────────────────────────────────
def chart_smr_saving_scatter(df: pd.DataFrame, out_dir: str):
    base = df[df["Glass Scenario"] == "base"].copy()
    fig = go.Figure()
    for smr, label in SCENARIO_LABELS.items():
        sub = base[base["SMR Scenario"] == smr]
        fig.add_trace(go.Scatter(
            mode="markers+text",
            name=label,
            x=sub["Saving vs Grid ($M)"],
            y=sub["Total TCO ($M)"],
            marker=dict(size=sub["ExaFLOPS"] * 6 + 12, color=COLORS[smr], opacity=0.85,
                         line=dict(width=1.5, color="white")),
            text=[SYSTEM_LABELS.get(s, s) for s in sub["System ID"]],
            textposition="top center",
            hovertemplate="<b>%{text}</b><br>절감: $%{x:,.0f}M<br>TCO: $%{y:,.0f}M<extra></extra>",
        ))
    fig.add_vline(x=0, line_dash="dash", line_color="gray", opacity=0.5)
    fig.update_layout(
        **LAYOUT_BASE,
        title=dict(
            text="SMR Saving vs Total TCO — Bubble = ExaFLOPS Scale<br>"
                 "<span style='font-size:14px;font-weight:normal'>Source: P6 Model | Right = more savings</span>",
            x=0.5, xanchor="center",
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
    )
    fig.update_xaxes(title_text="SMR 절감액 ($M)")
    fig.update_yaxes(title_text="Total TCO ($M)")
    fig.update_traces(cliponaxis=False)
    return save_chart(fig, "p6_smr_saving_scatter", out_dir,
                      "SMR 절감액 vs 총 TCO 산점도 (P6)",
                      "SMR 시나리오별 절감액과 총 TCO의 산점도. 버블 크기 = ExaFLOPS 규모")


# ────────────────────────────────────────
# 차트 5: Glass 채택률별 Substrate 비용 추이
# ────────────────────────────────────────
def chart_glass_adoption_line(df: pd.DataFrame, out_dir: str):
    # Glass 시나리오가 있는 경우만 (단일 SMR, SYS_B 기준)
    sub_smr = "smr_full"
    systems = ["SYS_A", "SYS_B", "SYS_C"]
    glass_scenarios = {"conservative": "보수 (15%)", "base": "기본 (35%)", "aggressive": "적극 (60%)"}

    fig = go.Figure()
    scenario_colors = ["#6366f1", "#10b981", "#f59e0b"]
    for i, (g_key, g_label) in enumerate(glass_scenarios.items()):
        sub = df[(df["SMR Scenario"] == sub_smr) & (df["Glass Scenario"] == g_key)]
        if sub.empty:
            continue
        fig.add_trace(go.Scatter(
            mode="lines+markers",
            name=g_label,
            x=[SYSTEM_LABELS.get(s, s) for s in sub["System ID"]],
            y=sub["CAPEX Glass/Pkg ($M)"],
            marker=dict(size=10, color=scenario_colors[i]),
            line=dict(width=2.5, color=scenario_colors[i]),
            hovertemplate=f"<b>{g_label}</b>: $%{{y:,.0f}}M<extra></extra>",
        ))
    fig.update_layout(
        **LAYOUT_BASE,
        title=dict(
            text="Glass Substrate Adoption — Cost by System & Scenario<br>"
                 "<span style='font-size:14px;font-weight:normal'>Source: P6 Model | SMR Full 기준</span>",
            x=0.5, xanchor="center",
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
    )
    fig.update_xaxes(title_text="System")
    fig.update_yaxes(title_text="Substrate/Pkg ($M)")
    return save_chart(fig, "p6_glass_adoption", out_dir,
                      "Glass 채택 시나리오별 기판 비용 추이 (P6)",
                      "보수/기본/적극 Glass 채택률에 따른 시스템별 기판+패키징 비용")


# ────────────────────────────────────────
# 메인
# ────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="P6 ExaFLOPS TCO 시각화")
    parser.add_argument("--json",  default="p6_exaflops_tco.json", help="JSON 입력 파일")
    parser.add_argument("--out",   default="output/p6_charts",     help="차트 출력 디렉토리")
    args = parser.parse_args()

    # JSON 파일 없으면 모델 직접 실행
    if not os.path.exists(args.json):
        print(f"[INFO] {args.json} 없음 → exaflops_resource_model.py 직접 실행")
        import subprocess, sys
        subprocess.run(
            [sys.executable, str(Path(__file__).parent / "exaflops_resource_model.py")],
            check=True
        )

    print(f"\n📂 JSON 로드: {args.json}")
    with open(args.json, "r", encoding="utf-8") as f:
        data = json.load(f)

    rows = []
    for r in data:
        rows.append({
            "System ID":              r["system_id"],
            "System Name":            r["system_name"],
            "ExaFLOPS":               r["exaflops"],
            "SMR Scenario":           r["smr_scenario"],
            "Glass Scenario":         r["glass_scenario"],
            "Lifetime (Y)":           r["lifetime_years"],
            "CAPEX HBM ($M)":         r["capex_hbm_usd_m"],
            "CAPEX Glass/Pkg ($M)":   r["capex_glass_pkg_usd_m"],
            "CAPEX Power Infra ($M)": r["capex_power_infra_usd_m"],
            "CAPEX GPU/Other ($M)":   r["capex_gpu_other_usd_m"],
            "Total CAPEX ($M)":       r["total_capex_usd_m"],
            "OPEX Power ($M)":        r["opex_power_usd_m"],
            "OPEX Maintenance ($M)":  r["opex_maintenance_usd_m"],
            "OPEX Other ($M)":        r["opex_other_usd_m"],
            "Total OPEX ($M)":        r["total_opex_usd_m"],
            "Total TCO ($M)":         r["total_tco_usd_m"],
            "TCO/ExaFLOPS ($M)":      r["tco_per_exaflops_usd_m"],
            "Saving vs Grid ($M)":    r["saving_vs_grid_only_usd_m"],
            "MOIC Contribution":      r["moic_contribution"],
        })
    df = pd.DataFrame(rows)

    print(f"\n📈 차트 생성 시작 → {args.out}")
    chart_tco_stacked(df, args.out)
    chart_cost_per_exaflops(df, args.out)
    chart_layer_breakdown(df, args.out)
    chart_smr_saving_scatter(df, args.out)
    chart_glass_adoption_line(df, args.out)
    print(f"\n✅ 5개 차트 완료 → {args.out}/")


if __name__ == "__main__":
    main()
