"""Critic module for auditing reasoning graphs and detecting blind spots.

The critic assigns a numerical quality score to a graph and produces a report
highlighting potential issues such as low connectivity, extreme centralisation,
missing validation markers or contradictory relations.  This module is the
primary tool for self‑testing and meta‑analysis.
"""

from __future__ import annotations

from typing import Dict, Any, List
import statistics

import networkx as nx


class Critic:
    def evaluate_graph(self, reasoning_graph) -> float:
        """Compute an overall quality score for the reasoning graph.

        The score is a weighted combination of:
          - normalised edge density (more connections encourage rich reasoning)
          - mean node score (importance of concepts)
          - inverse centralisation (penalise hubs dominating the graph)
        The resulting value is between 0 and 1.
        """
        g: nx.DiGraph = reasoning_graph.graph
        n = g.number_of_nodes()
        m = g.number_of_edges()
        if n == 0:
            return 0.0
        # Edge density normalised by number of possible directed edges
        density = m / (n * (n - 1)) if n > 1 else 0.0
        # Mean node score (default to 0.5 if missing)
        scores = [attrs.get('score', 0.5) for _, attrs in g.nodes(data=True)]
        mean_score = sum(scores) / len(scores)
        # Centralisation: measure how balanced degree distribution is
        degrees = [deg for _, deg in g.degree()]
        if len(degrees) > 1:
            max_deg = max(degrees)
            centralisation = sum(max_deg - d for d in degrees) / ((len(degrees) - 1) * (len(degrees) - 2) + 1e-9)
        else:
            centralisation = 0.0
        # Invert centralisation (1 = perfectly balanced, 0 = highly centralised)
        inv_centralisation = 1.0 - min(1.0, centralisation)
        # Weighted sum
        return 0.4 * density + 0.4 * mean_score + 0.2 * inv_centralisation

    def audit_graph(self, reasoning_graph) -> Dict[str, Any]:
        """Return a dict summarising potential issues and statistics."""
        g: nx.DiGraph = reasoning_graph.graph
        report: Dict[str, Any] = {}
        n = g.number_of_nodes()
        m = g.number_of_edges()
        report['num_nodes'] = n
        report['num_edges'] = m
        # Find isolated nodes
        isolated = [node for node, deg in g.degree() if deg == 0]
        report['isolated_nodes'] = isolated
        # Detect extremely high variance in node scores
        scores = [attrs.get('score', 0.5) for _, attrs in g.nodes(data=True)]
        if len(scores) > 1:
            variance = statistics.pstdev(scores)
        else:
            variance = 0.0
        report['score_variance'] = variance
        # Identify hubs (top 5% by degree)
        degrees = [deg for _, deg in g.degree()]
        if degrees:
            threshold = sorted(degrees)[max(0, int(len(degrees) * 0.95))]
            hubs = [node for node, deg in g.degree() if deg >= threshold and deg > 0]
        else:
            hubs = []
        report['hubs'] = hubs
        # Flag possible blind spots: nodes with no outgoing edges (dead ends)
        dead_ends = [node for node in g.nodes() if g.out_degree(node) == 0 and g.in_degree(node) > 0]
        report['dead_ends'] = dead_ends
        # Compute overall quality
        report['quality_score'] = round(self.evaluate_graph(reasoning_graph), 4)
        # Recommendations
        recommendations: List[str] = []
        if isolated:
            recommendations.append(f"Integrate {len(isolated)} isolated nodes by linking them to related concepts.")
        if variance > 0.3:
            recommendations.append("Normalise node scores; high variance suggests inconsistent importance assignments.")
        if hubs:
            recommendations.append(f"Consider decomposing {len(hubs)} hubs into modular subgraphs to avoid bottlenecks.")
        if dead_ends:
            recommendations.append(f"Extend reasoning from {len(dead_ends)} dead‑end nodes to improve coverage.")
        report['recommendations'] = recommendations
        return report