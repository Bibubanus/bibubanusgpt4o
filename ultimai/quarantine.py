"""Quarantine module for isolating low‑quality reasoning nodes.

Nodes with a score below a given threshold are tagged as quarantined.  They
can later be reintegrated when their score improves above a reintegration
threshold.
"""

from __future__ import annotations

from typing import List

from .graph import ReasoningGraph


class Quarantine:
    """Maintain a list of quarantined node identifiers."""

    def __init__(self, threshold: float = 0.35) -> None:
        self.threshold = threshold
        self.quarantined: List[str] = []

    def evaluate(self, reasoning_graph: ReasoningGraph) -> List[str]:
        """Evaluate nodes and quarantine those with score below the threshold."""
        for node, attrs in list(reasoning_graph.graph.nodes(data=True)):  # type: ignore
            score = attrs.get("score", 0.5)
            if score is not None and score < self.threshold and node not in self.quarantined:
                self.quarantined.append(node)
                reasoning_graph.graph.nodes[node]["quarantined"] = True
        return self.quarantined

    def reintegrate(self, reasoning_graph: ReasoningGraph, min_score: float = 0.5) -> List[str]:
        """Reintegrate quarantined nodes whose score has improved."""
        reintegrated: List[str] = []
        for node in list(self.quarantined):
            score = reasoning_graph.graph.nodes[node].get("score", 0.0)
            if score is not None and score >= min_score:
                reasoning_graph.graph.nodes[node]["quarantined"] = False
                self.quarantined.remove(node)
                reintegrated.append(node)
        return reintegrated