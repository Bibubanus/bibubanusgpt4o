"""Tests for the MemeticEngine in ultimai.reasoning_modulator."""

import random

from ultimai.graph import ReasoningGraph, NodeData
from ultimai.reasoning_modulator import MemeticEngine


def build_graph() -> ReasoningGraph:
    rg = ReasoningGraph()
    rg.add_node("A", NodeData(label="A", score=0.5))
    rg.add_node("B", NodeData(label="B", score=0.5))
    rg.add_node("C", NodeData(label="C", score=0.5))
    rg.add_edge("A", "B")
    rg.add_edge("B", "C")
    rg.add_edge("A", "C")
    return rg


def test_memetic_does_not_change_node_count() -> None:
    random.seed(42)
    rg = build_graph()
    engine = MemeticEngine(rg)
    initial_nodes = set(rg.graph.nodes)
    engine.run(iterations=3)
    assert set(rg.graph.nodes) == initial_nodes


def test_memetic_scores_within_bounds() -> None:
    random.seed(123)
    rg = build_graph()
    engine = MemeticEngine(rg)
    engine.run(iterations=5)
    for _, attrs in rg.graph.nodes(data=True):  # type: ignore
        score = attrs.get('score')
        assert 0.0 <= score <= 1.0