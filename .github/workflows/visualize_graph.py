#!/usr/bin/env python3
"""Render a reasoning graph to an image.

This script loads a graph saved by the reasoning infrastructure and
produces a PNG (or other supported format) showing the nodes and edges.
It falls back to NetworkX drawing if PyGraphviz is unavailable.

Usage:
  python visualize_graph.py --graph path/to/graph.json --output graph.png
"""

import argparse
from pathlib import Path
import json

import networkx as nx

from ultimai.graph_manager import ReasoningGraph


def draw_with_matplotlib(g: nx.DiGraph, output: str) -> None:
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(g, seed=42)
    labels = {n: data.get('label', n) for n, data in g.nodes(data=True)}
    nx.draw(g, pos, labels=labels, with_labels=True, node_size=500, font_size=8)
    plt.tight_layout()
    plt.savefig(output)
    plt.close()


def draw_with_graphviz(g: nx.DiGraph, output: str) -> bool:
    try:
        import pygraphviz as pgv
    except ImportError:
        return False
    A = nx.nx_agraph.to_agraph(g)
    A.layout('dot')
    A.draw(output)
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Visualise a reasoning graph")
    parser.add_argument('--graph', required=True, help='Path to the graph JSON file')
    parser.add_argument('--output', required=True, help='Output image file (e.g., graph.png)')
    args = parser.parse_args()

    rg = ReasoningGraph()
    rg.load(args.graph)
    g = rg.graph
    out_path = args.output
    if not draw_with_graphviz(g, out_path):
        print("pygraphviz not available; drawing with matplotlib...")
        draw_with_matplotlib(g, out_path)
    print(f"Graph image saved to {out_path}")


if __name__ == '__main__':
    main()