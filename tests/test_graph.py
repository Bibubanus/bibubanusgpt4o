"""Tests for the ReasoningGraph in ultimai.graph."""

from ultimai.graph import ReasoningGraph, NodeData
import math


def test_add_nodes_and_edges() -> None:
    rg = ReasoningGraph()
    rg.add_node("X", NodeData(label="X concept", score=0.8))
    rg.add_node("Y", NodeData(label="Y concept", score=0.4))
    rg.add_edge("X", "Y", relation="supports", weight=0.9)
    assert "X" in rg.graph.nodes
    assert "Y" in rg.graph.nodes
    assert rg.graph.has_edge("X", "Y")
    attrs = rg.graph.get_edge_data("X", "Y")
    assert attrs["relation"] == "supports"
    assert math.isclose(attrs["weight"], 0.9, rel_tol=1e-6)


def test_centrality_and_metrics() -> None:
    rg = ReasoningGraph()
    rg.add_node("A", NodeData(label="A", score=0.5))
    rg.add_node("B", NodeData(label="B", score=0.5))
    rg.add_node("C", NodeData(label="C", score=0.5))
    rg.add_edge("A", "B")
    rg.add_edge("B", "C")
    dc = rg.compute_degree_centrality()
    bc = rg.compute_betweenness_centrality()
    pr = rg.compute_pagerank()
    assert len(dc) == len(bc) == len(pr) == 3
    assert math.isclose(sum(dc.values()), len(dc), rel_tol=1e-6)