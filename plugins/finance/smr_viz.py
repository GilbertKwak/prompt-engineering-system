#!/usr/bin/env python3
"""
smr_viz.py — PE-7 P4/P5
Generates 5 MOIC/TCO visualization charts as PNG files.
Usage:
  python smr_viz.py \
    --config plugins/finance/smr_power_config.yaml \
    --output-dir output/charts \
    --timestamp 20260426_160000 \
    --version v1.2 \
    --scenario all
"""
import argparse, os, json, sys
from pathlib import Path

# ── Optional: load config values for dynamic labels ──────────
def load_config(config_path: str) -> dict:
    try:
        import yaml
        with open(config_path) as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--config",     required=True)
    p.add_argument("--output-dir", required=True)
    p.add_argument("--timestamp",  default="")
    p.add_argument("--version",    default="v1.2")
    p.add_argument("--scenario",   default="all")
    return p.parse_args()


def save_chart(fig, name: str, out_dir: Path, caption: str, description: str = ""):
    path = out_dir / f"{name}.png"
    fig.write_image(str(path), scale=2)
    meta = {"caption": caption, "description": description}
    with open(str(path) + ".meta.json", "w") as f:
        json.dump(meta, f)
    print(f"  ✅ {name}.png")
    return path


def generate_all_charts(out_dir: Path, cfg: dict, timestamp: str, version: str, scenario: str):
    import plotly.graph_objects as go
    import numpy as np

    NAVY   = "#1B2A4A"
    TEAL   = "#0D9488"
    AMBER  = "#D97706"
    RED    = "#DC2626"
    PURPLE = "#7C3AED"
    GRAY   = "#6B7280"
    BLUE   = "#2563EB"

    SUBTITLE = f"PE-7 P4 | {version} | {timestamp}"
    COMMON = dict(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Inter, Arial", size=13),
    )

    # ── Data ─────────────────────────────────────────────────
    types     = ["Type A", "Type B", "Type C", "Portfolio"]
    moic_grid = [1.11, 8.90, 11.50, 6.43]
    moic_part = [1.19, 9.47, 12.23, 6.97]
    moic_full = [1.30, 10.33, 13.43, 7.83]

    # 1. MOIC Grouped Bar
    fig1 = go.Figure()
    for vals, name, col in [
        (moic_grid, "Grid Only",   GRAY),
        (moic_part, "SMR Partial", TEAL),
        (moic_full, "SMR Full",    PURPLE),
    ]:
        fig1.add_trace(go.Bar(
            name=name, x=types, y=vals,
            marker_color=col,
            text=[f"{v:.2f}x" for v in vals],
            textposition="outside", textfont=dict(size=11),
        ))
    fig1.update_layout(
        title=dict(text=f"MOIC by Investment Type & SMR Scenario<br><sup>{SUBTITLE}</sup>"),
        barmode="group",
        xaxis_title="Investment Type", yaxis_title="MOIC (x)",
        yaxis_range=[0, 16],
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        height=460, margin=dict(l=60, r=40, t=100, b=60), **COMMON,
    )
    save_chart(fig1, "moic_grouped_bar", out_dir,
               f"MOIC Absolute by Type & SMR Scenario ({version})",
               "Grouped bar chart comparing MOIC across Grid/Partial/Full SMR scenarios.")

    # 2. MOIC Delta Bar
    delta_part = [v - b for v, b in zip(moic_part, moic_grid)]
    delta_full = [v - b for v, b in zip(moic_full, moic_grid)]
    fig2 = go.Figure()
    for vals, name, col in [(delta_part, "SMR Partial Δ", TEAL), (delta_full, "SMR Full Δ", PURPLE)]:
        fig2.add_trace(go.Bar(
            name=name, x=types, y=vals, marker_color=col,
            text=[f"+{v:.2f}x" for v in vals],
            textposition="outside", textfont=dict(size=12),
        ))
    fig2.update_layout(
        title=dict(text=f"MOIC Uplift Δ vs Grid Only<br><sup>{SUBTITLE}</sup>"),
        barmode="group",
        xaxis_title="Investment Type", yaxis_title="ΔMOIC (x)",
        yaxis_range=[0, 2.5],
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        height=420, margin=dict(l=60, r=40, t=100, b=60), **COMMON,
    )
    save_chart(fig2, "moic_delta_bar", out_dir,
               f"MOIC Delta Uplift vs Grid Only ({version})",
               "SMR Partial and Full MOIC uplift delta over Grid Only baseline.")

    # 3. Waterfall
    fig3 = go.Figure(go.Waterfall(
        orientation="v",
        measure=["absolute", "relative", "relative", "relative", "total"],
        x=["Grid", "Partial\n+1.2pp", "Full\n+2.8pp", "CAPEX\nAdj", "Net Full"],
        y=[6.43, 0.54, 0.86, -0.43, 7.40],
        text=["6.43x", "+0.54x", "+0.86x", "−0.43x", "7.40x"],
        textposition="outside",
        textfont=dict(size=13, color=NAVY),
        connector=dict(line=dict(color="#CBD5E1", width=1.5, dash="dot")),
        increasing=dict(marker=dict(color=TEAL)),
        decreasing=dict(marker=dict(color=RED)),
        totals=dict(marker=dict(color=PURPLE)),
    ))
    fig3.add_hline(y=6.43, line_dash="dash", line_color=GRAY, line_width=1.2,
                   annotation_text="Baseline 6.43x", annotation_position="top right",
                   annotation_font=dict(size=10, color=GRAY))
    fig3.update_layout(
        title=dict(text=f"Portfolio MOIC Waterfall: Grid → SMR Full<br><sup>{SUBTITLE}</sup>"),
        xaxis_title="Stage", yaxis_title="Portfolio MOIC (x)",
        yaxis_range=[0, 9.0], showlegend=False,
        height=460, margin=dict(l=70, r=60, t=100, b=60), **COMMON,
    )
    save_chart(fig3, "moic_waterfall", out_dir,
               f"Portfolio MOIC Waterfall: Grid to SMR Full ({version})",
               "Waterfall: Grid 6.43x + SMR Partial + SMR Full - CAPEX = 7.40x Net.")

    # 4. TCO Heatmap
    def calc_npv(grid_p, smr_lcoe, smr_pct, ann_gwh, dr=0.08, years=10):
        delta = grid_p - smr_lcoe
        ann = delta * ann_gwh * smr_pct * 1e3
        return sum(ann / (1+dr)**t for t in range(1, years+1)) / 1e6

    tiers = [
        ("HBM Fab (A)",    1800,  95),
        ("Glass Fab (A)",   950,  90),
        ("AI DC TW (B)",   4200,  78),
        ("AI DC US (C)",   8760,  65),
        ("AI DC EU (C)",   3500, 110),
    ]
    prices = list(range(65, 110, 5))
    z = [[round(calc_npv(p, 74, 0.80, gwh), 0) for p in prices]
         for _, gwh, _ in tiers]
    tier_labels = [t[0] for t in tiers]
    price_labels = [f"${p}" for p in prices]

    fig4 = go.Figure(go.Heatmap(
        z=z, x=price_labels, y=tier_labels,
        colorscale=[[0,"#FEE2E2"],[0.3,"#FEF3C7"],[0.6,"#CCFBF1"],[1.0,"#0D9488"]],
        text=[[f"${v:,.0f}M" for v in row] for row in z],
        texttemplate="%{text}", textfont=dict(size=12),
        showscale=True,
        colorbar=dict(title="NPV ($M)", thickness=16, len=0.8),
        xgap=4, ygap=4,
    ))
    fig4.update_layout(
        title=dict(text=f"TCO NPV Savings: Tier × Elec Price (RR SMR 80%)<br><sup>{SUBTITLE}</sup>"),
        xaxis_title="Grid Price ($/MWh)", yaxis_title="Facility Tier",
        height=460, margin=dict(l=130, r=100, t=100, b=60), **COMMON,
    )
    save_chart(fig4, "tco_heatmap", out_dir,
               f"TCO NPV Savings Heatmap by Facility Tier × Electricity Price ({version})",
               "NPV 10Y savings ($M) for RR SMR at 80% penetration across facility tiers and grid prices.")

    # 5. Bubble Chart
    port_pts = [
        {"name": "Grid Only",   "alpha": 0.0, "moic": 6.43, "net": 0,   "col": GRAY},
        {"name": "SMR Partial", "alpha": 1.2, "moic": 6.97, "net": 180, "col": TEAL},
        {"name": "SMR Full",    "alpha": 2.8, "moic": 7.83, "net": 470, "col": PURPLE},
    ]
    fig5 = go.Figure()
    fig5.add_trace(go.Scatter(
        x=[d["alpha"] for d in port_pts], y=[d["moic"] for d in port_pts],
        mode="lines", line=dict(color="#CBD5E1", width=1.5, dash="dot"),
        showlegend=False, hoverinfo="skip",
    ))
    for d in port_pts:
        sz = max(28, int(d["net"] / 6) + 28)
        fig5.add_trace(go.Scatter(
            x=[d["alpha"]], y=[d["moic"]],
            mode="markers+text",
            name=d["name"],
            marker=dict(size=sz, color=d["col"], opacity=0.85,
                        line=dict(width=2, color="white")),
            text=[f"{d['name']}\n{d['moic']:.2f}x"],
            textposition="top center", textfont=dict(size=11, color=NAVY),
        ))
    fig5.add_annotation(
        x=1.2, y=6.97, text="⭐ Best<br>+$180M Alpha",
        showarrow=True, arrowhead=2, arrowcolor=TEAL, ax=70, ay=-55,
        font=dict(size=11, color=TEAL), bgcolor="#F0FDF4",
        bordercolor=TEAL, borderwidth=1.5, borderpad=4,
    )
    fig5.update_layout(
        title=dict(text=f"IRR Alpha vs MOIC (Bubble = Net Alpha $M)<br><sup>{SUBTITLE}</sup>"),
        xaxis_title="SMR IRR Alpha (pp)", yaxis_title="MOIC (x)",
        xaxis=dict(range=[-0.4, 4.2]), yaxis=dict(range=[0, 10]),
        legend=dict(orientation="v", x=0.02, y=0.98, xanchor="left", yanchor="top",
                    bgcolor="rgba(255,255,255,0.85)",
                    bordercolor="#E5E7EB", borderwidth=1),
        height=500, margin=dict(l=70, r=80, t=100, b=60),
        paper_bgcolor="white", plot_bgcolor="#F9FAFB",
        font=dict(family="Inter, Arial", size=13),
    )
    save_chart(fig5, "irr_moic_bubble", out_dir,
               f"IRR Alpha vs Portfolio MOIC Bubble ({version})",
               "Portfolio bubbles sized by Net Alpha $M across Grid/Partial/Full SMR scenarios.")


def main():
    args = parse_args()
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    cfg = load_config(args.config)

    print(f"🎨 Generating SMR charts → {out_dir}")
    print(f"   Version: {args.version} | Timestamp: {args.timestamp} | Scenario: {args.scenario}")

    generate_all_charts(out_dir, cfg, args.timestamp, args.version, args.scenario)

    chart_files = list(out_dir.glob("*.png"))
    print(f"\n✅ {len(chart_files)} charts saved to {out_dir}")


if __name__ == "__main__":
    main()
