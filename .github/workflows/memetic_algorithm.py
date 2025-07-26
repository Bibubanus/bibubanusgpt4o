"""Memetic algorithm implementation for evolving reasoning graphs.

Memetic algorithms combine population‑based global search (akin to genetic
algorithms) with local optimisation (hill climbing).  In this simplified
implementation, we treat a reasoning graph as a single individual and apply
variations to node scores and relationships to explore alternative reasoning
paths.  A critic evaluates each variant, and improvements are retained.

In practice, memetic algorithms may operate over populations of graphs or
reasoning sequences.  The implementation here is intentionally modest to
provide a template for further development.
"""

from __future__ import annotations

import copy
import random
from typing import Dict, Tuple

from .graph_manager import ReasoningGraph
from .critic import Critic
from .utils import clamp


class MemeticEngine:
    """Run memetic evolution on a reasoning graph."""

    def __init__(self, graph: ReasoningGraph) -> None:
        self.graph = graph
        self.critic = Critic()

    def _mutate(self, g: ReasoningGraph) -> ReasoningGraph:
        """Return a mutated copy of the graph."""
        new_graph = copy.deepcopy(g)
        nodes = list(new_graph.graph.nodes(data=True))
        if not nodes:
            return new_graph
        # Select a random node and adjust its score slightly
        node_id, attrs = random.choice(nodes)
        current_score = attrs.get('score', 0.5)
        # Perturb score randomly within ±0.1
        new_score = clamp(current_score + random.uniform(-0.1, 0.1), 0.0, 1.0)
        new_graph.graph.nodes[node_id]['score'] = new_score
        # Occasionally add a new relation between random nodes
        if random.random() < 0.1 and len(nodes) > 1:
            n1, _ = random.choice(nodes)
            n2, _ = random.choice(nodes)
            if n1 != n2 and not new_graph.graph.has_edge(n1, n2):
                new_graph.add_edge(n1, n2, relation='suggests', weight=random.uniform(0.1, 1.0))
        return new_graph

    def _local_search(self, g: ReasoningGraph, iterations: int = 5) -> ReasoningGraph:
        """Perform a simple local search by greedily adjusting node scores."""
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
        """Run memetic evolution for a given number of iterations.

        The algorithm keeps the best variant found so far and gradually
        improves it using random mutations followed by local search.
        """
        current_graph = copy.deepcopy(self.graph)
        current_score = self.critic.evaluate_graph(current_graph)
        for i in range(iterations):
            mutated = self._mutate(current_graph)
            # Local search around mutated individual
            improved = self._local_search(mutated)
            improved_score = self.critic.evaluate_graph(improved)
            if improved_score > current_score:
                current_graph = improved
                current_score = improved_score
        # Replace the original graph with the evolved one
        self.graph.graph = current_graph.graph