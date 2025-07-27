#!/usr/bin/env python3
"""Dump an audit report for a reasoning graph.

This script loads a graph saved in JSON format, runs the critic to
produce an audit report and writes the report to a markdown file.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ultimai.graph import ReasoningGraph
from ultimai.critic import Critic


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an audit report for a reasoning graph")
    parser.add_argument('--graph', required=True, help='Path to the graph JSON file')
    parser.add_argument('--output', required=True, help='Output markdown file')
    args = parser.parse_args()
    rg = ReasoningGraph()
    rg.load(Path(args.graph))
    critic = Critic()
    report = critic.audit_graph(rg)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('# Audit Report\n\n')
        for key, value in report.items():
            f.write(f'**{key}**: {value}\n\n')
    print(f"Report saved to {out_path}")


if __name__ == '__main__':
    main()