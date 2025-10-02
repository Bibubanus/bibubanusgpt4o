#!/usr/bin/env python3
"""Example script to build a reasoning graph from a CSV file.

Usage:
  python build_graph.py --input my_data.csv --output my_graph.json

The CSV should contain columns describing relationships between concepts.
See `analysis/cross_reference_log.md` for the expected schema.
"""

import argparse
from pathlib import Path

from ultimai.graph_manager import ReasoningGraph


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a reasoning graph from CSV data")
    parser.add_argument('--input', required=True, help='CSV file with concept relationships')
    parser.add_argument('--output', required=True, help='Output JSON file for the graph')
    args = parser.parse_args()

    rg = ReasoningGraph()
    rg.from_csv(Path(args.input))
    rg.save(args.output)
    print(f"Graph saved to {args.output}")


if __name__ == '__main__':
    main()