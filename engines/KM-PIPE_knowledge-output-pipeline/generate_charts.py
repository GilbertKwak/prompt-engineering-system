#!/usr/bin/env python3
"""
generate_charts.py — KM-PIPE v3.0 · A7 VisualizationAgent
===========================================================
300dpi 고해상도 차트 자동 생성기 (Tufte 원칙 적용)
KM-PIPE Knowledge-to-Output Pipeline의 VisualizationAgent 실체 구현

사용법:
    python generate_charts.py --input data.json --output-dir reports/charts/
    python generate_charts.py --demo
    python generate_charts.py --input data.json --type line --title "HBM 시장 추이"

Tufte 원칙:
    - 데이터-잉크 비율 최대화 (불필요한 격자선/배경 제거)
    - Small Multiples 우선
    - 파이차트 금지 → 수평 막대 대체
    - 직접 레이블링 (범례 최소화)

Ref: T-09/KM-PIPE-MASTER-v3.0, engines/KM-PIPE_knowledge-output-pipeline/
"""

import argparse
import json
import os
import sys
import warnings
from datetime import datetime
from pathlib import Path

warnings.filterwarnings("ignore")

try:
    import matplotlib
    matplotlib.use("Agg")  # headless 환경 대응
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker
    from matplotlib.gridspec import GridSpec
except ImportError:
    print("[ERROR] matplotlib not installed. Run: pip install matplotlib")
    sys.exit(1)

try:
    import numpy as np
except ImportError:
    print("[ERROR] numpy not installed. Run: pip install numpy")
    sys.exit(1)

try:
    import networkx as nx
    HAS_NETWORKX = True
except ImportError:
    HAS_NETWORKX = False
    print("[WARN] networkx not installed. Concept graph 비활성화. pip install networkx")


# ─────────────────────────────────────────────
# TUFTE STYLE CONFIGURATION
# ─────────────────────────────────────────────
TUFTE_STYLE = {
    # 색상 팔레트 (Nexus Design System 기반)
    "colors": [
        "#01696F",  # Hydra Teal (primary)
        "#437A22",  # Gridania Green
        "#006494",  # Limsa Blue
        "#7A39BB",  # Kuja Purple
        "#DA7101",  # Costa Orange
        "#D19900",  # Altana Gold
        "#A12C7B",  # Error Maroon
        "#28251D",  # Sylph Gray (dark)
    ],
    "bg_color": "#FAFAF8",
    "text_color": "#28251D",
    "muted_color": "#7A7974",
    "grid_color": "#DCD9D5",
    "spine_color": "#D4D1CA",
    # 폰트
    "font_family": "DejaVu Sans",
    "title_size": 14,
    "label_size": 11,
    "tick_size": 9,
    "annotation_size": 9,
    # 해상도
    "dpi": 300,
    "figsize_default": (12, 7),
    "figsize_wide": (16, 8),
    "figsize_square": (10, 10),
}


def apply_tufte_style(ax):
    """Tufte 원칙: 스파인 최소화, 격자선 제거"""
    ax.set_facecolor(TUFTE_STYLE["bg_color"])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(TUFTE_STYLE["spine_color"])
    ax.spines["bottom"].set_color(TUFTE_STYLE["spine_color"])
    ax.tick_params(colors=TUFTE_STYLE["muted_color"], labelsize=TUFTE_STYLE["tick_size"])
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    # 수평 참조선만 (매우 연하게)
    ax.yaxis.grid(True, linestyle="-", alpha=0.25, color=TUFTE_STYLE["grid_color"], linewidth=0.6)
    ax.set_axisbelow(True)


def save_chart(fig, output_dir: str, filename: str) -> dict:
    """SVG + PNG 동시 저장 (300dpi)"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    stem = Path(filename).stem
    png_path = os.path.join(output_dir, f"{stem}.png")
    svg_path = os.path.join(output_dir, f"{stem}.svg")

    fig.savefig(png_path, dpi=TUFTE_STYLE["dpi"], bbox_inches="tight",
                facecolor=TUFTE_STYLE["bg_color"], edgecolor="none")
    fig.savefig(svg_path, format="svg", bbox_inches="tight",
                facecolor=TUFTE_STYLE["bg_color"], edgecolor="none")
    plt.close(fig)

    png_kb = os.path.getsize(png_path) / 1024
    svg_kb = os.path.getsize(svg_path) / 1024
    print(f"[OK] PNG: {png_path} ({png_kb:.0f} KB) | SVG: {svg_path} ({svg_kb:.0f} KB)")
    return {"png": png_path, "svg": svg_path}


# ─────────────────────────────────────────────
# CHART GENERATORS
# ─────────────────────────────────────────────

def chart_line(data: dict, output_dir: str, filename: str = "line_chart") -> dict:
    """
    라인 차트 — 시계열/추이 데이터
    data format: {"labels": [...], "series": [{"name": "", "values": [...]}]}
    """
    labels = data.get("labels", [])
    series = data.get("series", [])
    title = data.get("title", "Time Series Chart")
    x_label = data.get("x_label", "")
    y_label = data.get("y_label", "")

    fig, ax = plt.subplots(figsize=TUFTE_STYLE["figsize_default"])
    fig.patch.set_facecolor(TUFTE_STYLE["bg_color"])
    apply_tufte_style(ax)

    x = np.arange(len(labels))

    for i, s in enumerate(series):
        color = TUFTE_STYLE["colors"][i % len(TUFTE_STYLE["colors"])]
        vals = s.get("values", [])
        ax.plot(x, vals, color=color, linewidth=2.2, marker="o",
                markersize=5, markerfacecolor="white", markeredgewidth=1.8,
                markeredgecolor=color, label=s.get("name", f"Series {i+1}"),
                zorder=3)
        # 직접 레이블 (마지막 포인트)
        if vals:
            ax.annotate(
                f"{s.get('name', '')}: {vals[-1]:,.1f}",
                xy=(x[-1], vals[-1]),
                xytext=(8, 0), textcoords="offset points",
                fontsize=TUFTE_STYLE["annotation_size"],
                color=color, va="center",
            )

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=30 if len(labels) > 6 else 0,
                       ha="right" if len(labels) > 6 else "center")
    ax.set_title(title, fontsize=TUFTE_STYLE["title_size"],
                 color=TUFTE_STYLE["text_color"], fontweight="bold", pad=16)
    if x_label:
        ax.set_xlabel(x_label, fontsize=TUFTE_STYLE["label_size"],
                      color=TUFTE_STYLE["muted_color"])
    if y_label:
        ax.set_ylabel(y_label, fontsize=TUFTE_STYLE["label_size"],
                      color=TUFTE_STYLE["muted_color"])

    # 범례는 시리즈가 3개 이상일 때만 표시 (Tufte: 직접 레이블 우선)
    if len(series) > 3:
        ax.legend(frameon=False, fontsize=TUFTE_STYLE["annotation_size"],
                  labelcolor=TUFTE_STYLE["text_color"])

    plt.tight_layout()
    return save_chart(fig, output_dir, filename)


def chart_bar_horizontal(data: dict, output_dir: str, filename: str = "bar_chart") -> dict:
    """
    수평 막대 차트 — 비교 데이터 (Tufte: 파이차트 대체)
    data format: {"categories": [...], "values": [...], "title": ""}
    """
    categories = data.get("categories", [])
    values = data.get("values", [])
    title = data.get("title", "Comparison Chart")
    x_label = data.get("x_label", "")
    color = data.get("color", TUFTE_STYLE["colors"][0])

    # 값 기준 정렬 (Tufte: 알파벳순 또는 크기순)
    if data.get("sort", True) and categories and values:
        paired = sorted(zip(values, categories))
        values, categories = zip(*paired)
        values, categories = list(values), list(categories)

    fig, ax = plt.subplots(figsize=(10, max(4, len(categories) * 0.55 + 2)))
    fig.patch.set_facecolor(TUFTE_STYLE["bg_color"])
    apply_tufte_style(ax)
    ax.yaxis.grid(False)
    ax.xaxis.grid(True, linestyle="-", alpha=0.25,
                  color=TUFTE_STYLE["grid_color"], linewidth=0.6)

    y_pos = np.arange(len(categories))
    bars = ax.barh(y_pos, values, color=color, alpha=0.85, height=0.6)

    # 데이터 레이블
    for bar, val in zip(bars, values):
        ax.text(
            bar.get_width() + max(values) * 0.01, bar.get_y() + bar.get_height() / 2,
            f"{val:,.1f}", va="center", fontsize=TUFTE_STYLE["annotation_size"],
            color=TUFTE_STYLE["text_color"],
        )

    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories, fontsize=TUFTE_STYLE["tick_size"])
    ax.set_title(title, fontsize=TUFTE_STYLE["title_size"],
                 color=TUFTE_STYLE["text_color"], fontweight="bold", pad=16)
    if x_label:
        ax.set_xlabel(x_label, fontsize=TUFTE_STYLE["label_size"],
                      color=TUFTE_STYLE["muted_color"])
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)

    plt.tight_layout()
    return save_chart(fig, output_dir, filename)


def chart_scatter(data: dict, output_dir: str, filename: str = "scatter_chart") -> dict:
    """
    산점도 — 분포/상관관계 (trend line 포함)
    data format: {"x": [...], "y": [...], "labels": [...], "title": ""}
    """
    x_vals = data.get("x", [])
    y_vals = data.get("y", [])
    point_labels = data.get("labels", [])
    title = data.get("title", "Scatter Plot")
    x_label = data.get("x_label", "X")
    y_label = data.get("y_label", "Y")

    fig, ax = plt.subplots(figsize=TUFTE_STYLE["figsize_default"])
    fig.patch.set_facecolor(TUFTE_STYLE["bg_color"])
    apply_tufte_style(ax)

    ax.scatter(x_vals, y_vals, color=TUFTE_STYLE["colors"][0],
               s=80, alpha=0.8, zorder=3,
               edgecolors="white", linewidth=0.8)

    # 포인트 레이블
    for i, lbl in enumerate(point_labels):
        if i < len(x_vals) and i < len(y_vals):
            ax.annotate(
                lbl, (x_vals[i], y_vals[i]),
                xytext=(6, 6), textcoords="offset points",
                fontsize=TUFTE_STYLE["annotation_size"] - 1,
                color=TUFTE_STYLE["muted_color"],
            )

    # 추세선 (numpy polyfit)
    if len(x_vals) >= 3:
        try:
            z = np.polyfit(x_vals, y_vals, 1)
            p = np.poly1d(z)
            x_line = np.linspace(min(x_vals), max(x_vals), 100)
            ax.plot(x_line, p(x_line), "--", color=TUFTE_STYLE["colors"][1],
                    linewidth=1.4, alpha=0.7, label="Trend")
            ax.legend(frameon=False, fontsize=TUFTE_STYLE["annotation_size"])
        except Exception:
            pass

    ax.set_xlabel(x_label, fontsize=TUFTE_STYLE["label_size"],
                  color=TUFTE_STYLE["muted_color"])
    ax.set_ylabel(y_label, fontsize=TUFTE_STYLE["label_size"],
                  color=TUFTE_STYLE["muted_color"])
    ax.set_title(title, fontsize=TUFTE_STYLE["title_size"],
                 color=TUFTE_STYLE["text_color"], fontweight="bold", pad=16)

    plt.tight_layout()
    return save_chart(fig, output_dir, filename)


def chart_small_multiples(data: dict, output_dir: str,
                          filename: str = "small_multiples") -> dict:
    """
    Small Multiples — Tufte의 핵심 원칙 구현
    동일한 차트를 여러 카테고리에 걸쳐 비교
    data format: {"panels": [{"title": "", "labels": [...], "values": [...]}]}
    """
    panels = data.get("panels", [])
    main_title = data.get("title", "Small Multiples")
    n = len(panels)
    if n == 0:
        return {}

    cols = min(3, n)
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 5 + 1, rows * 3.5 + 1))
    fig.patch.set_facecolor(TUFTE_STYLE["bg_color"])
    fig.suptitle(main_title, fontsize=TUFTE_STYLE["title_size"] + 1,
                 color=TUFTE_STYLE["text_color"], fontweight="bold", y=1.02)

    axes_flat = np.array(axes).flatten() if n > 1 else [axes]

    for i, panel in enumerate(panels):
        ax = axes_flat[i]
        labels = panel.get("labels", [])
        values = panel.get("values", [])
        color = TUFTE_STYLE["colors"][i % len(TUFTE_STYLE["colors"])]

        apply_tufte_style(ax)
        ax.bar(range(len(labels)), values, color=color, alpha=0.8, width=0.6)
        ax.set_title(panel.get("title", f"Panel {i+1}"),
                     fontsize=TUFTE_STYLE["label_size"],
                     color=TUFTE_STYLE["text_color"], fontweight="bold")
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=30, ha="right",
                           fontsize=TUFTE_STYLE["tick_size"] - 1)

    # 빈 패널 숨기기
    for j in range(len(panels), len(axes_flat)):
        axes_flat[j].set_visible(False)

    plt.tight_layout()
    return save_chart(fig, output_dir, filename)


def chart_concept_graph(nodes: list, edges: list, output_dir: str,
                        filename: str = "concept_graph",
                        title: str = "Knowledge Graph") -> dict:
    """
    networkx 기반 개념 관계도
    수치 데이터 없을 때 자동 대체 차트
    nodes: [{"id": "", "label": "", "type": ""}]
    edges: [{"source": "", "target": "", "label": ""}]
    """
    if not HAS_NETWORKX:
        print("[WARN] networkx 없음 — concept graph 건너뜀")
        return {}

    G = nx.DiGraph()
    node_colors = []
    node_labels = {}
    type_color_map = {
        "engine": TUFTE_STYLE["colors"][0],
        "report": TUFTE_STYLE["colors"][2],
        "domain": TUFTE_STYLE["colors"][1],
        "concept": TUFTE_STYLE["colors"][3],
        "default": TUFTE_STYLE["colors"][7],
    }

    for node in nodes:
        nid = node.get("id", node.get("label", str(node)))
        G.add_node(nid)
        node_labels[nid] = node.get("label", nid)
        ntype = node.get("type", "default")
        node_colors.append(type_color_map.get(ntype, type_color_map["default"]))

    edge_labels = {}
    for edge in edges:
        src = edge.get("source", "")
        tgt = edge.get("target", "")
        if src and tgt:
            G.add_edge(src, tgt)
            lbl = edge.get("label", "")
            if lbl:
                edge_labels[(src, tgt)] = lbl

    fig, ax = plt.subplots(figsize=TUFTE_STYLE["figsize_square"])
    fig.patch.set_facecolor(TUFTE_STYLE["bg_color"])
    ax.set_facecolor(TUFTE_STYLE["bg_color"])
    ax.axis("off")

    pos = nx.spring_layout(G, seed=42, k=2.0)
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=800,
                           alpha=0.9, ax=ax)
    nx.draw_networkx_labels(G, pos, labels=node_labels,
                            font_size=8, font_color=TUFTE_STYLE["bg_color"],
                            font_weight="bold", ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color=TUFTE_STYLE["grid_color"],
                           arrows=True, arrowsize=15,
                           connectionstyle="arc3,rad=0.1",
                           width=1.2, alpha=0.8, ax=ax)
    if edge_labels:
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                                     font_size=7,
                                     font_color=TUFTE_STYLE["muted_color"],
                                     ax=ax)

    ax.set_title(title, fontsize=TUFTE_STYLE["title_size"],
                 color=TUFTE_STYLE["text_color"], fontweight="bold", pad=16)
    plt.tight_layout()
    return save_chart(fig, output_dir, filename)


# ─────────────────────────────────────────────
# AUTO-DETECT CHART TYPE FROM KM-PIPE OUTPUT
# ─────────────────────────────────────────────
def auto_generate_from_km_pipe(pipeline_data: dict, output_dir: str) -> list:
    """
    KM-PIPE pipeline output에서 차트 데이터를 자동 감지하여 생성
    Returns: 생성된 차트 파일 경로 목록
    """
    results = []
    viz = pipeline_data.get("visualization", {})
    notion = pipeline_data.get("notion_data", {})
    word_struct = pipeline_data.get("word_doc_structure", {})
    title_base = notion.get("title", "report")

    chart_type = viz.get("chart_type", "")
    chart_data = viz.get("chart_data", {})

    if chart_data:
        if chart_type == "line":
            r = chart_line(chart_data, output_dir, f"{title_base}_line")
        elif chart_type in ("bar", "horizontal_bar"):
            r = chart_bar_horizontal(chart_data, output_dir, f"{title_base}_bar")
        elif chart_type == "scatter":
            r = chart_scatter(chart_data, output_dir, f"{title_base}_scatter")
        elif chart_type == "small_multiples":
            r = chart_small_multiples(chart_data, output_dir, f"{title_base}_multiples")
        else:
            # 기본: 수평 막대
            r = chart_bar_horizontal(chart_data, output_dir, f"{title_base}_bar")
        results.append(r)

    # KG 그래프 자동 생성 (kg_delta 있을 경우)
    kg_data = pipeline_data.get("kg_delta", {})
    if kg_data.get("edges"):
        edges = kg_data["edges"]
        new_node = kg_data.get("new_node_id", "NEW")
        nodes = [{"id": new_node, "label": new_node, "type": "concept"}]
        for edge in edges:
            for key in ("source", "target"):
                nid = edge.get(key, "")
                if nid and nid not in [n["id"] for n in nodes]:
                    nodes.append({"id": nid, "label": nid, "type": "concept"})
        r = chart_concept_graph(nodes, edges, output_dir, f"{title_base}_kg")
        if r:
            results.append(r)

    return results


# ─────────────────────────────────────────────
# DEMO
# ─────────────────────────────────────────────
def run_demo(output_dir: str = "reports/charts/demo"):
    """HBM 시장 데이터 샘플 차트 전체 생성 데모"""
    print(f"[DEMO] Tufte 스타일 차트 생성 중... 출력 폴더: {output_dir}")
    results = []

    # 1. 라인 차트 — HBM 시장 성장 추이
    line_data = {
        "title": "HBM 시장 규모 추이 (2022–2026)",
        "x_label": "연도",
        "y_label": "시장 규모 (억 달러)",
        "labels": ["2022", "2023", "2024", "2025", "2026E"],
        "series": [
            {"name": "SK하이닉스", "values": [42, 68, 112, 178, 245]},
            {"name": "삼성전자", "values": [28, 45, 78, 132, 188]},
            {"name": "마이크론", "values": [12, 22, 45, 72, 98]},
        ],
    }
    results.append(chart_line(line_data, output_dir, "hbm_market_trend"))

    # 2. 수평 막대 — 시장점유율 비교
    bar_data = {
        "title": "HBM 공급업체 시장점유율 (2026 Q2)",
        "x_label": "점유율 (%)",
        "sort": True,
        "categories": ["SK하이닉스", "삼성전자", "마이크론"],
        "values": [52, 33, 15],
        "color": "#01696F",
    }
    results.append(chart_bar_horizontal(bar_data, output_dir, "hbm_market_share"))

    # 3. 산점도 — 가격 vs 대역폭
    scatter_data = {
        "title": "HBM 세대별 성능-비용 포지셔닝",
        "x_label": "대역폭 (GB/s)",
        "y_label": "단가 지수 (HBM2=100)",
        "x": [410, 819, 1230, 1638, 2200],
        "y": [100, 145, 195, 270, 380],
        "labels": ["HBM2", "HBM2E", "HBM3", "HBM3E", "HBM4"],
    }
    results.append(chart_scatter(scatter_data, output_dir, "hbm_perf_cost"))

    # 4. Small Multiples — 분기별 출하량
    sm_data = {
        "title": "HBM 분기별 출하량 추이 — 업체별 비교",
        "panels": [
            {"title": "SK하이닉스", "labels": ["Q1", "Q2", "Q3", "Q4"],
             "values": [58, 65, 74, 88]},
            {"title": "삼성전자", "labels": ["Q1", "Q2", "Q3", "Q4"],
             "values": [32, 38, 44, 52]},
            {"title": "마이크론", "labels": ["Q1", "Q2", "Q3", "Q4"],
             "values": [18, 22, 26, 31]},
        ],
    }
    results.append(chart_small_multiples(sm_data, output_dir, "hbm_quarterly_sm"))

    # 5. 개념 관계도 — KG 노드
    nodes = [
        {"id": "KM-PIPE", "label": "KM-PIPE v3.0", "type": "engine"},
        {"id": "C-38", "label": "C-38 PE-INTEL", "type": "report"},
        {"id": "C-37", "label": "C-37 AI Ecosystem", "type": "report"},
        {"id": "HBM4", "label": "HBM4 노드", "type": "domain"},
        {"id": "PE-1", "label": "PE-1 자동개선", "type": "engine"},
        {"id": "PE-3", "label": "PE-3 자동검증", "type": "engine"},
    ]
    edges = [
        {"source": "KM-PIPE", "target": "C-38", "label": "feeds"},
        {"source": "KM-PIPE", "target": "C-37", "label": "feeds"},
        {"source": "C-38", "target": "HBM4", "label": "monitors"},
        {"source": "PE-1", "target": "KM-PIPE", "label": "refines"},
        {"source": "PE-3", "target": "KM-PIPE", "label": "validates"},
    ]
    r = chart_concept_graph(nodes, edges, output_dir, "km_pipe_kg",
                            title="KM-PIPE v3.0 — Knowledge Graph 연결 구조")
    if r:
        results.append(r)

    print(f"\n[DEMO COMPLETE] {len(results)}개 차트 생성 완료")
    for r in results:
        if isinstance(r, dict):
            for fmt, path in r.items():
                print(f"  {fmt.upper()}: {path}")
    return results


# ─────────────────────────────────────────────
# CLI ENTRY POINT
# ─────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="KM-PIPE v3.0 · A7 VisualizationAgent — 300dpi Tufte 차트 자동 생성",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  python generate_charts.py --demo
  python generate_charts.py --input km_pipe_output.json --output-dir reports/charts/
  python generate_charts.py --type line --data '{"title": "Test", "labels": ["A","B"], "series": [{"name": "S1", "values": [1,2]}]}'
        """,
    )
    parser.add_argument("--input", "-i", help="KM-PIPE JSON output 파일")
    parser.add_argument("--output-dir", "-o", default="reports/charts", help="출력 디렉토리")
    parser.add_argument("--type", "-t",
                        choices=["line", "bar", "scatter", "small_multiples", "concept_graph", "auto"],
                        default="auto", help="차트 타입")
    parser.add_argument("--data", "-d", help="인라인 JSON 데이터 (--type 지정 시 사용)")
    parser.add_argument("--title", help="차트 제목")
    parser.add_argument("--demo", action="store_true", help="HBM 샘플 데모 실행")
    parser.add_argument("--dpi", type=int, default=300, help="출력 DPI (기본값: 300)")

    args = parser.parse_args()

    if args.dpi != 300:
        TUFTE_STYLE["dpi"] = args.dpi

    if args.demo:
        run_demo(os.path.join(args.output_dir, "demo"))
        return

    if args.input:
        if not os.path.exists(args.input):
            print(f"[ERROR] 입력 파일 없음: {args.input}")
            sys.exit(1)
        with open(args.input, "r", encoding="utf-8") as f:
            pipeline_data = json.load(f)
        results = auto_generate_from_km_pipe(pipeline_data, args.output_dir)
        print(f"[DONE] {len(results)}개 차트 생성 완료")
        return

    if args.data:
        chart_data = json.loads(args.data)
        if args.title:
            chart_data["title"] = args.title
        chart_func = {
            "line": chart_line,
            "bar": chart_bar_horizontal,
            "scatter": chart_scatter,
            "small_multiples": chart_small_multiples,
        }.get(args.type, chart_bar_horizontal)
        chart_func(chart_data, args.output_dir, args.type + "_chart")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
