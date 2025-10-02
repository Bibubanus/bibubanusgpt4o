#!/usr/bin/env python3
"""
Command line interface for running common tasks in the ULTIMAI reasoning infrastructure.

Usage:
  python cli.py build-graph --input FILE --output FILE
  python cli.py run-memetic --graph FILE --iterations N
  python cli.py run-audit --graph FILE
  python cli.py run-quarantine --graph FILE --threshold FLOAT

This CLI exposes a few high‑level commands for constructing graphs, executing memetic algorithms
and running self‑audits.  More advanced workflows can be orchestrated via the MetaAgent class
or customised scripts in the `scripts` directory.
"""

import argparse
import json
from pathlib import Path

from ultimai.graph_manager import ReasoningGraph
from ultimai.memetic_algorithm import MemeticEngine
from ultimai.critic import Critic
from ultimai.quarantine import Quarantine


def cmd_build_graph(args: argparse.Namespace) -> None:
    """Build a reasoning graph from a CSV or JSON file and save it."""
    rg = ReasoningGraph()
    input_path = Path(args.input)
    if input_path.suffix.lower() == '.csv':
        rg.from_csv(input_path)
    elif input_path.suffix.lower() in {'.json', '.jsonl'}:
        rg.from_json(input_path)
    else:
        raise ValueError(f"Unsupported input format: {input_path.suffix}")
    rg.save(args.output)
    print(f"Graph with {rg.graph.number_of_nodes()} nodes and {rg.graph.number_of_edges()} edges saved to {args.output}")


def cmd_run_memetic(args: argparse.Namespace) -> None:
    """Run the memetic algorithm on an existing graph."""
    rg = ReasoningGraph()
    rg.load(args.graph)
    engine = MemeticEngine(rg)
    engine.run(iterations=args.iterations)
    rg.save(args.graph)  # persist modifications to the graph
    print(f"Memetic algorithm completed. Updated graph saved to {args.graph}")


def cmd_run_audit(args: argparse.Namespace) -> None:
    """Run critic audit on an existing graph and print a summary."""
    rg = ReasoningGraph()
    rg.load(args.graph)
    critic = Critic()
    report = critic.audit_graph(rg)
    # Save to file or print
    print(json.dumps(report, indent=2, ensure_ascii=False))


def cmd_run_quarantine(args: argparse.Namespace) -> None:
    """Evaluate quarantine rules on the graph and output quarantined nodes."""
    rg = ReasoningGraph()
    rg.load(args.graph)
    quarantine = Quarantine(threshold=args.threshold)
    quarantined = quarantine.evaluate(rg)
    if quarantined:
        print(f"Nodes moved to quarantine: {quarantined}")
    else:
        print("No nodes met the quarantine threshold.")


def main() -> None:
    parser = argparse.ArgumentParser(description="ULTIMAI reasoning infrastructure CLI")
    subparsers = parser.add_subparsers(dest='command', required=True)
    # build-graph
    p_build = subparsers.add_parser('build-graph', help='Construct a reasoning graph from input data')
    p_build.add_argument('--input', required=True, help='Path to CSV or JSON input file')
    p_build.add_argument('--output', required=True, help='Path to save the generated graph (JSON)')
    p_build.set_defaults(func=cmd_build_graph)
    # run-memetic
    p_memetic = subparsers.add_parser('run-memetic', help='Run memetic evolution on an existing graph')
    p_memetic.add_argument('--graph', required=True, help='Path to the graph JSON file')
    p_memetic.add_argument('--iterations', type=int, default=10, help='Number of memetic iterations')
    p_memetic.set_defaults(func=cmd_run_memetic)
    # run-audit
    p_audit = subparsers.add_parser('run-audit', help='Run critic audit on a graph')
    p_audit.add_argument('--graph', required=True, help='Path to the graph JSON file')
    p_audit.set_defaults(func=cmd_run_audit)
    # run-quarantine
    p_quarantine = subparsers.add_parser('run-quarantine', help='Apply quarantine rules to a graph')
    p_quarantine.add_argument('--graph', required=True, help='Path to the graph JSON file')
    p_quarantine.add_argument('--threshold', type=float, default=0.35, help='Variance threshold for quarantine')
    p_quarantine.set_defaults(func=cmd_run_quarantine)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()