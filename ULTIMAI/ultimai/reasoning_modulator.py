"""Memetic algorithm (reasoning modulator) for evolving reasoning graphs.

This module implements a simple memetic algorithm that mutates node scores
and occasionally adds new relations between nodes.  A critic is used to
evaluate candidate graphs, and improvements are retained.  The algorithm
operates on a single reasoning graph instance.
"""

from __future__ import annotations

import copy
import random
from typing import Tuple

from .graph import ReasoningGraph
from .critic import Critic
from .utils import clamp


class MemeticEngine:
    """Run memetic evolution on a reasoning graph."""

    def __init__(self, graph: ReasoningGraph) -> None:
        self.graph = graph
        self.critic = Critic()

    def _mutate(self, g: ReasoningGraph) -> ReasoningGraph:
        new_graph = copy.deepcopy(g)
        nodes = list(new_graph.graph.nodes(data=True))  # type: ignore
        if not nodes:
            return new_graph
        node_id, attrs = random.choice(nodes)
        current_score = attrs.get("score", 0.5)
        new_score = clamp(current_score + random.uniform(-0.1, 0.1), 0.0, 1.0)
        new_graph.graph.nodes[node_id]["score"] = new_score
        # Occasionally add new relation
        if random.random() < 0.1 and len(nodes) > 1:
            n1, _ = random.choice(nodes)
            n2, _ = random.choice(nodes)
            if n1 != n2 and not new_graph.graph.has_edge(n1, n2):
                new_graph.add_edge(n1, n2, relation="suggests", weight=random.uniform(0.1, 1.0))
        return new_graph

    def _local_search(self, g: ReasoningGraph, iterations: int = 5) -> ReasoningGraph:
        best_graph = copy.deepcopy(g)
        best_score = self.critic.evaluate_graph(best_graph)
        for _ in range(iterations):
            candidate = self._mutate(best_graph)
            cand_score = self.critic.evaluate_graph(candidate)
            if cand_score > best_score:
                best_graph = candidate
                best_score = cand_score
        return best_graph

    def run(self, iterations: int = 10) -> None:
        current_graph = copy.deepcopy(self.graph)
        current_score = self.critic.evaluate_graph(current_graph)
        for _ in range(iterations):
            mutated = self._mutate(current_graph)
            improved = self._local_search(mutated)
            improved_score = self.critic.evaluate_graph(improved)
            if improved_score > current_score:
                current_graph = improved
                current_score = improved_score
        self.graph.graph = current_graph.graph