"""Quarantine module for isolating low‑quality reasoning nodes.

The quarantine is a temporary storage for nodes that fall below a given quality
threshold.  Nodes can be re‑evaluated and reintegrated after further evidence
or context is obtained.  The quarantine threshold is typically based on the
`score` attribute of nodes or other heuristics.
"""

from __future__ import annotations

from typing import List

from .graph_manager import ReasoningGraph


class Quarantine:
    def __init__(self, threshold: float = 0.35) -> None:
        self.threshold = threshold
        self.quarantined: List[str] = []

    def evaluate(self, reasoning_graph: ReasoningGraph) -> List[str]:
        """Evaluate nodes and quarantine those with scores below the threshold.

        Returns a list of node identifiers that were quarantined.  Quarantined
        nodes remain in the graph, but could be handled separately by other
        modules (e.g. ignored in memetic evolution) and tagged for review.
        """
        for node, attrs in list(reasoning_graph.graph.nodes(data=True)):
            score = attrs.get('score', 0.5)
            if score < self.threshold and node not in self.quarantined:
                self.quarantined.append(node)
                # Tag node as quarantined
                reasoning_graph.graph.nodes[node]['quarantined'] = True
        return self.quarantined

    def reintegrate(self, reasoning_graph: ReasoningGraph, min_score: float = 0.5) -> List[str]:
        """Attempt to reintegrate quarantined nodes whose score has improved."""
        reintegrated: List[str] = []
        for node in list(self.quarantined):
            score = reasoning_graph.graph.nodes[node].get('score', 0.0)
            if score >= min_score:
                reasoning_graph.graph.nodes[node]['quarantined'] = False
                self.quarantined.remove(node)
                reintegrated.append(node)
        return reintegrated