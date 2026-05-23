#!/usr/bin/env python3
"""
generate_charts.py — KM-PIPE Visualization Agent (A7)
Knowledge-to-Output Pipeline v3.0

Usage:
  python generate_charts.py --input <json_file> --output-dir <charts/>
  python generate_charts.py --data '{"labels":[...],"values":[...]}' --type bar --output chart.png

Part of: engines/KM-PIPE_knowledge-output-pipeline/
Linked engines: PE-1, PE-2, PE-3
Notion ref: T-09 > PE-IP > KM-PIPE-MASTER-v3.0
GitHub: engines/KM-PIPE_knowledge-output-pipeline/generate_charts.py
Tufte principles: data-ink maximization, no chartjunk, small multiples
Author: GilbertKwak (KM-PIPE v3.0)
Date: 2026-05-23
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import matplotlib
    matplotlib.use("Agg")  # Non-interactive backend (server/CI safe)
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    from matplotlib.patches import FancyBboxPatch
except ImportError:
    print("[ERROR] matplotlib not installed. Run: pip install matplotlib")
    sys.exit(1)

try:
    import numpy as np
except ImportError:
    print("[ERROR] numpy not installed. Run: pip install numpy")
    sys.exit(1)


# ─────────────────────────────────────────────────────────
# CONSTANTS & TUFTE STYLE
# ─────────────────────────────────────────────────────────
VERSION = "3.0.0"
KM_PIPE_ENGINE = "KM-PIPE-A7-VisualizationAgent"

# Tufte-inspired style settings
TUFTE_STYLE = {
    "figure.facecolor": "#FAFAF8",
    "axes.facecolor": "#FAFAF8",
    "axes.edgecolor": "#CCCCCC",
    "axes.linewidth": 0.8,
    "axes.grid": True,
    "axes.grid.axis": "y",          # Horizontal gridlines only (Tufte)
    "grid.color": "#E8E8E8",
    "grid.linewidth": 0.5,
    "grid.linestyle": "-",
    "xtick.color": "#555555",
    "ytick.color": "#555555",
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "axes.labelsize": 10,
    "axes.labelcolor": "#333333",
    "axes.titlesize": 12,
    "axes.titlecolor": "#1A1A2E",
    "axes.titleweight": "bold",
    "axes.spines.top": False,       # Remove top spine (Tufte)
    "axes.spines.right": False,     # Remove right spine (Tufte)
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
    "legend.frameon": False,        # No legend box (Tufte)
    "legend.fontsize": 9,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.15,
}

# Domain-aware color palettes (Nexus Design System)
PALETTES = {
    "semiconductor": ["#01696F", "#0F3E60", "#437A22", "#964219", "#7A39BB"],
    "ai_infra":      ["#006494", "#01696F", "#7A39BB", "#437A22", "#D19900"],
    "investment":    ["#01696F", "#437A22", "#964219", "#A12C7B", "#006494"],
    "strategy":      ["#1A1A2E", "#01696F", "#964219", "#437A22", "#7A39BB"],
    "default":       ["#01696F", "#006494", "#437A22", "#964219", "#7A39BB"],
}

# Chart type aliases
CHART_ALIASES = {
    "bar": "bar", "horizontal_bar": "horizontal_bar", "hbar": "horizontal_bar",
    "line": "line", "timeseries": "line",
    "scatter": "scatter",
    "small_multiples": "small_multiples",
    "network": "network",
    "heatmap": "heatmap",
    "auto": "auto",
}


# ─────────────────────────────────────────────────────────
# TUFTE STYLE APPLICATOR
# ─────────────────────────────────────────────────────────
def apply_tufte_style():
    """Apply Tufte-inspired rcParams globally."""
    plt.rcParams.update(TUFTE_STYLE)


def tufte_despine(ax):
    """Remove top and right spines; offset remaining spines."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_position(("outward", 5))
    ax.spines["bottom"].set_position(("outward", 5))


def add_data_labels(ax, bars, fmt: str = "{:.1f}", fontsize: int = 8,
                    color: str = "#333333", offset: float = 0.01):
    """Add direct data labels to bars (Tufte: label > legend)."""
    y_max = ax.get_ylim()[1]
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.annotate(
                fmt.format(height),
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 4), textcoords="offset points",
                ha="center", va="bottom",
                fontsize=fontsize, color=color
            )


# ─────────────────────────────────────────────────────────
# CHART GENERATORS
# ─────────────────────────────────────────────────────────
class ChartGenerator:
    """A7 VisualizationAgent — generates Tufte-styled charts."""

    def __init__(self, domain: str = "default", verbose: bool = True):
        self.domain = domain if domain in PALETTES else "default"
        self.colors = PALETTES[self.domain]
        self.verbose = verbose
        apply_tufte_style()

    def _log(self, msg: str):
        if self.verbose:
            print(f"[A7-VizAgent] {msg}")

    def _save(self, fig, output_path: str, title: str = ""):
        """Save as PNG (300dpi) and SVG simultaneously."""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        base = str(output_path).rsplit(".", 1)[0]
        fig.savefig(output_path, dpi=300, format="png")
        fig.savefig(f"{base}.svg", format="svg")
        self._log(f"Saved: {output_path} + {base}.svg")
        plt.close(fig)
        return output_path

    def auto_detect_type(self, data: dict) -> str:
        """
        Tufte rule: chart type follows data structure.
        - time-indexed → line
        - comparison categories → horizontal_bar
        - two continuous vars → scatter
        - composition → small_multiples (NOT pie)
        """
        if "x" in data and "y" in data and len(data.get("x", [])) > 0:
            # Check if x looks like dates/time
            x_sample = str(data["x"][0]) if data["x"] else ""
            if any(c in x_sample for c in ["-", "/", "Q", "W", "20"]):
                return "line"
            return "scatter"
        if "labels" in data and "values" in data:
            n = len(data["labels"])
            if n <= 8:
                return "horizontal_bar"  # Easier comparison (Tufte)
            return "bar"
        if "series" in data:
            return "small_multiples"
        if "nodes" in data:
            return "network"
        if "matrix" in data:
            return "heatmap"
        return "bar"

    # ── BAR CHART (vertical)
    def bar(self, labels: list, values: list, title: str = "",
            xlabel: str = "", ylabel: str = "", output_path: str = "chart_bar.png") -> str:
        self._log(f"Generating bar chart: {title}")
        fig, ax = plt.subplots(figsize=(10, 6))
        x = np.arange(len(labels))
        bars = ax.bar(x, values, color=self.colors[0], width=0.65,
                      alpha=0.85, edgecolor="white", linewidth=0.5)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=30, ha="right")
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        add_data_labels(ax, bars)
        tufte_despine(ax)
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
        return self._save(fig, output_path, title)

    # ── HORIZONTAL BAR CHART (Tufte preferred for category comparison)
    def horizontal_bar(self, labels: list, values: list, title: str = "",
                        xlabel: str = "", output_path: str = "chart_hbar.png") -> str:
        self._log(f"Generating horizontal bar chart: {title}")
        # Sort by value (Tufte: visual order = data order)
        sorted_pairs = sorted(zip(values, labels), reverse=True)
        values_s = [p[0] for p in sorted_pairs]
        labels_s = [p[1] for p in sorted_pairs]

        fig, ax = plt.subplots(figsize=(10, max(5, len(labels) * 0.5 + 1)))
        y = np.arange(len(labels_s))
        bars = ax.barh(y, values_s, color=self.colors[0], height=0.65,
                       alpha=0.85, edgecolor="white", linewidth=0.5)
        ax.set_yticks(y)
        ax.set_yticklabels(labels_s)
        ax.set_xlabel(xlabel)
        ax.set_title(title)
        ax.invert_yaxis()
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.grid(axis="x", color="#E8E8E8", linewidth=0.5)
        ax.set_axisbelow(True)

        # Direct labels on bars
        for bar, val in zip(bars, values_s):
            ax.text(
                bar.get_width() + max(values_s) * 0.01, bar.get_y() + bar.get_height() / 2,
                f"{val:,.1f}", va="center", ha="left", fontsize=8, color="#333333"
            )
        return self._save(fig, output_path, title)

    # ── LINE CHART (time series)
    def line(self, x: list, y_series: dict, title: str = "",
              xlabel: str = "", ylabel: str = "",
              output_path: str = "chart_line.png") -> str:
        """
        y_series: {"Series Name": [values...], ...}
        """
        self._log(f"Generating line chart: {title}")
        fig, ax = plt.subplots(figsize=(11, 6))

        for i, (series_name, y_vals) in enumerate(y_series.items()):
            color = self.colors[i % len(self.colors)]
            ax.plot(x, y_vals, color=color, linewidth=2,
                    marker="o", markersize=4, label=series_name)
            # Direct label at end of line (Tufte: label > legend)
            if y_vals:
                ax.annotate(
                    series_name,
                    xy=(len(x) - 1, y_vals[-1]),
                    xytext=(5, 0), textcoords="offset points",
                    va="center", fontsize=8, color=color
                )

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        tufte_despine(ax)
        ax.xaxis.set_tick_params(rotation=30)
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
        return self._save(fig, output_path, title)

    # ── SCATTER CHART
    def scatter(self, x: list, y: list, labels: list = None,
                 title: str = "", xlabel: str = "", ylabel: str = "",
                 add_trendline: bool = True,
                 output_path: str = "chart_scatter.png") -> str:
        self._log(f"Generating scatter chart: {title}")
        fig, ax = plt.subplots(figsize=(10, 7))
        ax.scatter(x, y, color=self.colors[0], s=60, alpha=0.7,
                   edgecolors="white", linewidth=0.5)

        if labels:
            for xi, yi, lbl in zip(x, y, labels):
                ax.annotate(lbl, (xi, yi), xytext=(4, 4),
                            textcoords="offset points", fontsize=7,
                            color="#555555")

        if add_trendline and len(x) >= 3:
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            x_line = np.linspace(min(x), max(x), 100)
            ax.plot(x_line, p(x_line), "--", color=self.colors[1],
                    linewidth=1.2, alpha=0.7, label="Trend")

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        tufte_despine(ax)
        return self._save(fig, output_path, title)

    # ── SMALL MULTIPLES (Tufte's preferred over pie charts)
    def small_multiples(self, series_dict: dict, title: str = "",
                         ncols: int = 3, output_path: str = "chart_small_multiples.png") -> str:
        """
        series_dict: {
          "Category A": {"labels": [...], "values": [...]},
          "Category B": {"labels": [...], "values": [...]},
          ...
        }
        """
        self._log(f"Generating small multiples: {title}")
        n = len(series_dict)
        ncols = min(ncols, n)
        nrows = (n + ncols - 1) // ncols
        fig, axes = plt.subplots(nrows, ncols,
                                  figsize=(5 * ncols, 4 * nrows),
                                  constrained_layout=True)
        if n == 1:
            axes = [axes]
        elif nrows == 1:
            axes = list(axes)
        else:
            axes = [ax for row in axes for ax in row]

        for idx, (cat_name, cat_data) in enumerate(series_dict.items()):
            ax = axes[idx]
            labels = cat_data.get("labels", [])
            values = cat_data.get("values", [])
            color = self.colors[idx % len(self.colors)]
            x = np.arange(len(labels))
            bars = ax.bar(x, values, color=color, width=0.7,
                          alpha=0.85, edgecolor="white", linewidth=0.3)
            ax.set_title(cat_name, fontsize=10, fontweight="bold")
            ax.set_xticks(x)
            ax.set_xticklabels(labels, rotation=30, ha="right", fontsize=7)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.grid(axis="y", color="#EEEEEE", linewidth=0.4)

        # Hide unused axes
        for idx in range(n, len(axes)):
            axes[idx].set_visible(False)

        if title:
            fig.suptitle(title, fontsize=13, fontweight="bold", color="#1A1A2E",
                         y=1.02)
        return self._save(fig, output_path, title)

    # ── NETWORK / KNOWLEDGE GRAPH
    def network(self, nodes: list, edges: list, title: str = "",
                 output_path: str = "chart_network.png") -> str:
        """
        nodes: ["NodeA", "NodeB", ...]
        edges: [("NodeA", "NodeB", {"label": "RELATED_TO"}), ...]
        """
        try:
            import networkx as nx
        except ImportError:
            self._log("[WARN] networkx not installed. Skipping network chart.")
            return ""

        self._log(f"Generating network/KG chart: {title}")
        G = nx.DiGraph()
        G.add_nodes_from(nodes)
        for edge in edges:
            if len(edge) >= 2:
                G.add_edge(edge[0], edge[1],
                           label=edge[2].get("label", "") if len(edge) > 2 else "")

        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_facecolor("#FAFAF8")
        fig.patch.set_facecolor("#FAFAF8")

        pos = nx.spring_layout(G, seed=42, k=2.5)
        nx.draw_networkx_nodes(G, pos, ax=ax, node_size=800,
                               node_color=self.colors[0], alpha=0.9)
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=8,
                                font_color="white", font_weight="bold")
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#AAAAAA",
                               arrows=True, arrowsize=20,
                               connectionstyle="arc3,rad=0.1",
                               width=1.2, alpha=0.7)
        edge_labels = {(u, v): d.get("label", "") for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                                      ax=ax, font_size=7, font_color="#555555")
        ax.set_title(title, fontsize=12, fontweight="bold", color="#1A1A2E")
        ax.axis("off")
        return self._save(fig, output_path, title)

    # ── HEATMAP
    def heatmap(self, matrix: list, row_labels: list, col_labels: list,
                 title: str = "", output_path: str = "chart_heatmap.png") -> str:
        self._log(f"Generating heatmap: {title}")
        data = np.array(matrix)
        fig, ax = plt.subplots(figsize=(max(8, len(col_labels)), max(6, len(row_labels) * 0.6)))
        im = ax.imshow(data, cmap="YlOrBr", aspect="auto")
        ax.set_xticks(np.arange(len(col_labels)))
        ax.set_yticks(np.arange(len(row_labels)))
        ax.set_xticklabels(col_labels, rotation=45, ha="right")
        ax.set_yticklabels(row_labels)

        # Annotate cells
        for i in range(len(row_labels)):
            for j in range(len(col_labels)):
                val = data[i, j]
                text_color = "white" if val > data.max() * 0.6 else "#333333"
                ax.text(j, i, f"{val:.1f}", ha="center", va="center",
                        fontsize=8, color=text_color)

        plt.colorbar(im, ax=ax, shrink=0.8)
        ax.set_title(title, fontsize=12, fontweight="bold", color="#1A1A2E")
        ax.spines[:].set_visible(False)
        return self._save(fig, output_path, title)


# ─────────────────────────────────────────────────────────
# PIPELINE DISPATCHER — from KM-PIPE JSON
# ─────────────────────────────────────────────────────────
class ChartDispatcher:
    """Dispatch chart generation from full KM-PIPE JSON payload."""

    def __init__(self, output_dir: str = "charts", verbose: bool = True):
        self.output_dir = output_dir
        self.verbose = verbose
        Path(output_dir).mkdir(parents=True, exist_ok=True)

    def run(self, payload: dict) -> list:
        """Generate all charts defined in visualization.charts[]"""
        generated = []
        viz = payload.get("visualization", {})
        domain = payload.get("notion_data", {}).get("domain", "default")
        gen = ChartGenerator(domain=domain, verbose=self.verbose)

        charts = viz.get("charts", [])
        if not charts:
            # Fallback: try to auto-generate from notion_data
            charts = self._auto_generate_from_payload(payload)

        for i, chart_spec in enumerate(charts):
            chart_type = CHART_ALIASES.get(chart_spec.get("type", "auto"), "auto")
            if chart_type == "auto":
                chart_type = gen.auto_detect_type(chart_spec.get("data", {}))

            output_path = os.path.join(
                self.output_dir,
                chart_spec.get("filename", f"chart_{i+1:02d}_{chart_type}.png")
            )
            title = chart_spec.get("title", f"Chart {i+1}")
            data = chart_spec.get("data", {})

            try:
                path = self._dispatch_single(gen, chart_type, data, title, output_path)
                if path:
                    generated.append(path)
            except Exception as e:
                print(f"[A7-VizAgent][ERROR] Chart {i+1} ({chart_type}): {e}")

        return generated

    def _dispatch_single(self, gen: ChartGenerator, chart_type: str,
                          data: dict, title: str, output_path: str) -> Optional[str]:
        if chart_type == "bar":
            return gen.bar(data["labels"], data["values"], title=title,
                           xlabel=data.get("xlabel", ""), ylabel=data.get("ylabel", ""),
                           output_path=output_path)
        elif chart_type == "horizontal_bar":
            return gen.horizontal_bar(data["labels"], data["values"], title=title,
                                       xlabel=data.get("xlabel", ""),
                                       output_path=output_path)
        elif chart_type == "line":
            return gen.line(data["x"], data.get("y_series", {"Series": data.get("y", [])}),
                            title=title, xlabel=data.get("xlabel", ""),
                            ylabel=data.get("ylabel", ""), output_path=output_path)
        elif chart_type == "scatter":
            return gen.scatter(data["x"], data["y"], labels=data.get("labels"),
                               title=title, xlabel=data.get("xlabel", ""),
                               ylabel=data.get("ylabel", ""),
                               output_path=output_path)
        elif chart_type == "small_multiples":
            return gen.small_multiples(data["series"], title=title, output_path=output_path)
        elif chart_type == "network":
            return gen.network(data["nodes"], data["edges"], title=title, output_path=output_path)
        elif chart_type == "heatmap":
            return gen.heatmap(data["matrix"], data["row_labels"],
                               data["col_labels"], title=title, output_path=output_path)
        return None

    def _auto_generate_from_payload(self, payload: dict) -> list:
        """Auto-generate chart spec from key_points if no charts defined."""
        key_points = payload.get("notion_data", {}).get("key_points", [])
        if not key_points:
            return []
        # Create a simple horizontal bar from key_points scores (if numeric)
        return [{
            "type": "horizontal_bar",
            "title": "Key Points Overview",
            "filename": "chart_01_key_points.png",
            "data": {
                "labels": [str(kp)[:40] for kp in key_points[:8]],
                "values": list(range(len(key_points[:8]), 0, -1)),
                "xlabel": "Relevance Score"
            }
        }]


# ─────────────────────────────────────────────────────────
# CLI ENTRY POINT
# ─────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description=f"KM-PIPE VisualizationAgent v{VERSION} — Chart Generator (Tufte-styled, 300dpi)"
    )
    parser.add_argument("--input", "-i", help="KM-PIPE JSON payload file")
    parser.add_argument("--output-dir", "-o", default="charts", help="Output directory for charts")
    parser.add_argument("--type", "-t",
                        choices=["bar", "hbar", "line", "scatter", "small_multiples", "network", "heatmap", "auto"],
                        default="auto", help="Chart type")
    parser.add_argument("--data", "-d", help="Inline JSON data for quick mode")
    parser.add_argument("--title", default="Chart", help="Chart title")
    parser.add_argument("--domain",
                        choices=["semiconductor", "ai_infra", "investment", "strategy", "default"],
                        default="default", help="Domain for color palette selection")
    parser.add_argument("--output", default="chart.png", help="Quick mode output filename")
    parser.add_argument("--quiet", "-q", action="store_true")
    args = parser.parse_args()

    if args.input:
        # Pipeline mode
        with open(args.input, "r", encoding="utf-8") as f:
            payload = json.load(f)
        dispatcher = ChartDispatcher(output_dir=args.output_dir, verbose=not args.quiet)
        generated = dispatcher.run(payload)
        print(f"✅ Generated {len(generated)} chart(s):")
        for p in generated:
            print(f"   → {p}")

    elif args.data:
        # Quick mode
        data = json.loads(args.data)
        gen = ChartGenerator(domain=args.domain, verbose=not args.quiet)
        chart_type = CHART_ALIASES.get(args.type, "auto")
        if chart_type == "auto":
            chart_type = gen.auto_detect_type(data)

        out_path = os.path.join(args.output_dir, args.output)
        dispatcher = ChartDispatcher(output_dir=args.output_dir, verbose=not args.quiet)
        path = dispatcher._dispatch_single(gen, chart_type, data, args.title, out_path)
        if path:
            print(f"✅ Chart saved: {path}")
        else:
            print("[ERROR] Chart generation failed.")
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
