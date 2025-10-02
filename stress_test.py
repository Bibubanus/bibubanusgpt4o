#!/usr/bin/env python3
"""Stress‑test the reasoning infrastructure.

This script constructs random reasoning graphs and applies memetic evolution,
quarantine and critic audits to explore failure modes and performance.

It is intended for experimentation and should not be used in production.
"""

import argparse
import random
from typing import List

from ultimai.graph_manager import ReasoningGraph
from ultimai.memetic_algorithm import MemeticEngine
from ultimai.quarantine import Quarantine
from ultimai.critic import Critic


from ultimai.graph_manager import NodeData


def generate_random_graph(num_nodes: int, num_edges: int) -> ReasoningGraph:
    rg = ReasoningGraph()
    for i in range(num_nodes):
        nid = f"N{i}"
        rg.add_node(nid, data=NodeData(label=f"Node {i}", score=random.uniform(0, 1)))  # type: ignore[arg-type]
    # random edges
    nodes = list(rg.graph.nodes())
    for _ in range(num_edges):
        src, dst = random.sample(nodes, 2)
        rg.add_edge(src, dst, relation=random.choice(['supports', 'contradicts', 'extends']), weight=random.uniform(0.1, 1.0))
    return rg


def run_stress_test(iterations: int, num_nodes: int, num_edges: int) -> None:
    critic = Critic()
    quarantine = Quarantine(threshold=0.3)
    scores: List[float] = []
    for i in range(iterations):
        rg = generate_random_graph(num_nodes, num_edges)
        engine = MemeticEngine(rg)
        engine.run(iterations=5)
        quarantine.evaluate(rg)
        report = critic.audit_graph(rg)
        scores.append(report['quality_score'])
        print(f"Iteration {i+1}/{iterations}: quality={report['quality_score']:.4f}, quarantined={len(quarantine.quarantined)}")
    avg_score = sum(scores) / len(scores)
    print(f"Average quality score over {iterations} iterations: {avg_score:.4f}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a memetic stress‑test on random graphs")
    parser.add_argument('--iterations', type=int, default=5, help='Number of stress‑test runs')
    parser.add_argument('--nodes', type=int, default=20, help='Number of nodes in each random graph')
    parser.add_argument('--edges', type=int, default=40, help='Number of edges in each random graph')
    args = parser.parse_args()
    run_stress_test(args.iterations, args.nodes, args.edges)


if __name__ == '__main__':
    main()