"""Critic module for auditing reasoning graphs.

The critic computes a quality score based on edge density, mean node score
and inverse centralisation.  It also reports isolated nodes, hubs, dead
ends and recommendations for improving the graph structure.
"""

from __future__ import annotations

from typing import Any, Dict, List
import statistics

try:
    import networkx as nx  # type: ignore
except ImportError:  # pragma: no cover
    from . import networkx_stub as nx  # type: ignore


class Critic:
    def evaluate_graph(self, reasoning_graph) -> float:
        g: nx.DiGraph = reasoning_graph.graph  # type: ignore
        n = g.number_of_nodes()
        m = g.number_of_edges()
        if n == 0:
            return 0.0
        density = m / (n * (n - 1)) if n > 1 else 0.0
        scores = [attrs.get('score', 0.5) for _, attrs in g.nodes(data=True)]  # type: ignore
        mean_score = sum(scores) / len(scores)
        degrees = [deg for _, deg in g.degree()]
        if len(degrees) > 1:
            max_deg = max(degrees)
            centralisation = sum(max_deg - d for d in degrees) / ((len(degrees) - 1) * (len(degrees) - 2) + 1e-9)
        else:
            centralisation = 0.0
        inv_centralisation = 1.0 - min(1.0, centralisation)
        return 0.4 * density + 0.4 * mean_score + 0.2 * inv_centralisation

    def audit_graph(self, reasoning_graph) -> Dict[str, Any]:
        g: nx.DiGraph = reasoning_graph.graph  # type: ignore
        report: Dict[str, Any] = {}
        n = g.number_of_nodes()
        m = g.number_of_edges()
        report['num_nodes'] = n
        report['num_edges'] = m
        isolated = [node for node, deg in g.degree() if deg == 0]
        report['isolated_nodes'] = isolated
        scores = [attrs.get('score', 0.5) for _, attrs in g.nodes(data=True)]  # type: ignore
        variance = statistics.pstdev(scores) if len(scores) > 1 else 0.0
        report['score_variance'] = variance
        degrees = [deg for _, deg in g.degree()]
        hubs: List[str] = []
        if degrees:
            threshold = sorted(degrees)[max(0, int(len(degrees) * 0.95))]
            hubs = [node for node, deg in g.degree() if deg >= threshold and deg > 0]
        report['hubs'] = hubs
        dead_ends = [node for node in g.nodes() if g.out_degree(node) == 0 and g.in_degree(node) > 0]  # type: ignore
        report['dead_ends'] = dead_ends
        report['quality_score'] = round(self.evaluate_graph(reasoning_graph), 4)
        recommendations: List[str] = []
        if isolated:
            recommendations.append(f"Integrate {len(isolated)} isolated nodes.")
        if variance > 0.3:
            recommendations.append("Normalise node scores; high variance detected.")
        if hubs:
            recommendations.append(f"Decompose {len(hubs)} hubs into subgraphs.")
        if dead_ends:
            recommendations.append(f"Extend reasoning from {len(dead_ends)} dead‑end nodes.")
        report['recommendations'] = recommendations
        return report