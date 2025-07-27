#!/usr/bin/env python3
"""Generate a reasoning graph from seed data and save it to JSON and optionally PNG/SVG.

This script reads the seed data from a JSON file in `data/seeds.json`,
builds a reasoning graph using the `ReasoningGraph` class and writes the
resulting graph to JSON.  It will attempt to render an image if
Graphviz or matplotlib is available.  When neither is available, it
falls back to a simple textual representation.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from ultimai.ingestion import ingest_json
from ultimai.graph import ReasoningGraph

# Use the same visualisation helpers as in the legacy script
try:
    import networkx as nx  # type: ignore
except ImportError:
    from ultimai import networkx_stub as nx  # type: ignore


def draw_graph(g: nx.DiGraph, output: str) -> None:  # type: ignore
    """Attempt to draw the graph using pygraphviz or matplotlib."""
    # Attempt Graphviz via pygraphviz
    try:
        import pygraphviz as pgv  # type: ignore
        if hasattr(nx, 'nx_agraph'):
            A = nx.nx_agraph.to_agraph(g)
            A.layout('dot')
            A.draw(output)
            print(f"Graph image saved to {output} using Graphviz")
            return
    except ImportError:
        pass
    # Fallback to matplotlib
    try:
        import matplotlib.pyplot as plt  # type: ignore
        if hasattr(nx, 'spring_layout') and hasattr(nx, 'draw'):
            pos = nx.spring_layout(g, seed=42)
            labels = {n: data.get('label', n) for n, data in g.nodes(data=True)}  # type: ignore
            plt.figure(figsize=(8, 6))
            nx.draw(g, pos, labels=labels, with_labels=True, node_size=500, font_size=8)
            plt.tight_layout()
            plt.savefig(output)
            plt.close()
            print(f"Graph image saved to {output} using matplotlib")
            return
    except ImportError:
        pass
    # Final fallback: write a text representation
    text_output = output + ".txt"
    with open(text_output, 'w', encoding='utf-8') as f:
        f.write("Nodes:\n")
        for n, attrs in g.nodes(data=True):  # type: ignore
            f.write(f"  {n}: {attrs}\n")
        f.write("Edges:\n")
        for u, v, attrs in g.edges(data=True):  # type: ignore
            f.write(f"  {u} -> {v}: {attrs}\n")
    print(f"Graph text saved to {text_output}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a reasoning graph from seed data")
    parser.add_argument('--input', required=True, help='Path to JSON seed file')
    parser.add_argument('--output', required=True, help='Output JSON file for the graph')
    args = parser.parse_args()
    rg = ingest_json(args.input)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    rg.save(out_path)
    # Attempt to draw an image alongside the JSON
    image_path = out_path.with_suffix('.png')
    draw_graph(rg.graph, str(image_path))  # type: ignore


if __name__ == '__main__':
    main()