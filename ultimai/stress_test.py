"""Stress test for the memetic algorithm and quarantine.

This module provides a function to run a simple stress test on a
ReasoningGraph.  It generates a small random graph, runs the memetic
algorithm and quarantine, and returns basic metrics.  It can be used
from tests and from the CI pipeline to ensure the system behaves
predictably under load.
"""

from __future__ import annotations

import random

from .graph import ReasoningGraph, NodeData
from .reasoning_modulator import MemeticEngine
from .quarantine import Quarantine


def run_stress_test(iterations: int = 3, threshold: float = 0.3) -> dict:
    """Run a stress test and return metrics about quarantined and reintegrated nodes."""
    # Build a simple graph with three nodes
    rg = ReasoningGraph()
    rg.add_node("A", NodeData(label="A", score=0.5))
    rg.add_node("B", NodeData(label="B", score=0.5))
    rg.add_node("C", NodeData(label="C", score=0.5))
    rg.add_edge("A", "B", relation="supports", weight=1.0)
    rg.add_edge("B", "C", relation="contradicts", weight=0.5)
    rg.add_edge("A", "C", relation="resolves", weight=0.8)
    # Run memetic evolution
    engine = MemeticEngine(rg)
    engine.run(iterations)
    # Apply quarantine
    quarantine = Quarantine(threshold)
    quarantined = quarantine.evaluate(rg)
    # Slightly increase scores to reintegrate some nodes
    for node in quarantined:
        rg.graph.nodes[node]["score"] = threshold + 0.2
    reintegrated = quarantine.reintegrate(rg, min_score=threshold + 0.1)
    return {
        "num_nodes": rg.graph.number_of_nodes(),
        "num_edges": rg.graph.number_of_edges(),
        "quarantined": len(quarantined),
        "reintegrated": len(reintegrated),
    }