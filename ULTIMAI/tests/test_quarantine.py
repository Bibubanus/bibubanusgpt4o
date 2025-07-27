"""Tests for the Quarantine module."""

from ultimai.graph import ReasoningGraph, NodeData
from ultimai.quarantine import Quarantine


def build_graph() -> ReasoningGraph:
    rg = ReasoningGraph()
    rg.add_node("A", NodeData(label="A", score=0.8))
    rg.add_node("B", NodeData(label="B", score=0.5))
    rg.add_node("C", NodeData(label="C", score=0.2))
    rg.add_edge("A", "B")
    rg.add_edge("B", "C")
    return rg


def test_quarantine_and_reintegration() -> None:
    rg = build_graph()
    quarantine = Quarantine(threshold=0.5)
    quarantined = quarantine.evaluate(rg)
    assert 'C' in quarantined
    assert rg.graph.nodes['C'].get('quarantined') is True
    # increase score and reintegrate
    rg.graph.nodes['C']['score'] = 0.6
    reintegrated = quarantine.reintegrate(rg, min_score=0.5)
    assert 'C' in reintegrated
    assert 'C' not in quarantine.quarantined
    assert rg.graph.nodes['C'].get('quarantined') is False