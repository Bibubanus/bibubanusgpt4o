"""Graph representation for the ULTIMAI reasoning infrastructure.

This module defines a simple directed reasoning graph with support for
loading data from CSV or JSON, adding nodes and edges, computing basic
centrality metrics and serialising the graph.  It attempts to use
NetworkX when available and falls back to a minimal stub when not.
"""

from __future__ import annotations

import json
import csv
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

# Attempt to import NetworkX; if unavailable, use a local stub.
try:
    import networkx as nx  # type: ignore
except ImportError:  # pragma: no cover
    from . import networkx_stub as nx  # type: ignore


@dataclass
class NodeData:
    """Data associated with a node in the reasoning graph."""
    label: str
    type: str = "concept"
    source: Optional[str] = None
    score: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None


class ReasoningGraph:
    """Container for a directed reasoning graph."""

    def __init__(self) -> None:
        self.graph: nx.DiGraph = nx.DiGraph()

    def add_node(self, node_id: str, data: NodeData) -> None:
        self.graph.add_node(node_id, **asdict(data))

    def add_edge(self, src: str, dst: str, relation: str = "influences", weight: float = 1.0) -> None:
        self.graph.add_edge(src, dst, relation=relation, weight=weight)

    def from_csv(self, path: Path) -> None:
        """Load nodes and edges from a CSV file with column names matching seeds.json."""
        records: List[Dict[str, Any]]
        try:
            import pandas as pd  # type: ignore
        except ImportError:
            pd = None  # type: ignore
        if pd is not None:
            df = pd.read_csv(path)
            records = df.to_dict(orient="records")
        else:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                records = [row for row in reader]
        for row in records:
            src = str(row.get("source_id")) if row.get("source_id") is not None else str(row.get("source_label"))
            dst = str(row.get("target_id")) if row.get("target_id") is not None else str(row.get("target_label"))
            if not self.graph.has_node(src):
                self.add_node(src, NodeData(
                    label=row.get("source_label", src),
                    type=row.get("source_type", "concept"),
                    source=row.get("source_file"),
                    score=float(row.get("source_score")) if row.get("source_score") not in (None, "") else None,
                    metadata={},
                ))
            if not self.graph.has_node(dst):
                self.add_node(dst, NodeData(
                    label=row.get("target_label", dst),
                    type=row.get("target_type", "concept"),
                    source=row.get("target_file"),
                    score=float(row.get("target_score")) if row.get("target_score") not in (None, "") else None,
                    metadata={},
                ))
            # Parse weight if present
            w = row.get("weight", 1.0)
            try:
                weight = float(w)
            except (TypeError, ValueError):
                weight = 1.0
            self.add_edge(src, dst, relation=row.get("relation", "influences"), weight=weight)

    def from_json(self, path: Path) -> None:
        """Load a graph from a JSON file saved by `save`.

        The file must contain a node‑link representation as produced by
        `networkx.readwrite.node_link_data`.
        """
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        g = nx.node_link_graph(data)  # type: ignore
        self.graph = g  # type: ignore

    def save(self, path: Path) -> None:
        """Save the graph to a JSON file in node‑link format."""
        data = nx.node_link_data(self.graph)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self, path: Path) -> None:
        """Alias for from_json."""
        self.from_json(path)

    # Basic metrics
    def compute_degree_centrality(self) -> Dict[str, float]:
        """Compute a degree-based centrality where the sum of scores equals the number of nodes.

        This method delegates to ``self.degree_centrality()`` for backward
        compatibility.  See ``degree_centrality`` for details.
        """
        return self.degree_centrality()

    def compute_betweenness_centrality(self) -> Dict[str, float]:
        return nx.betweenness_centrality(self.graph)

    def compute_pagerank(self, alpha: float = 0.85) -> Dict[str, float]:
        return nx.pagerank(self.graph, alpha=alpha)

    def get_neighbors(self, node_id: str) -> List[str]:
        return list(self.graph.neighbors(node_id))

    def subgraph(self, nodes: Iterable[str]) -> "ReasoningGraph":
        sg = ReasoningGraph()
        sg.graph = self.graph.subgraph(nodes).copy()
        return sg

    # ------------------------------------------------------------------
    # Centrality
    def degree_centrality(self) -> Dict[str, float]:
        """
        Compute degree centrality values for each node and normalise them so
        that the sum of all values equals the number of nodes ``n``.  This
        method aligns with our unit tests, which expect the centrality
        distribution to sum to the size of the graph.  When the graph has
        no nodes, an empty dictionary is returned.  For an edgeless graph
        (no edges), all nodes are assigned a uniform value of ``1.0`` so that
        their sum equals ``n``.

        Internally, if NetworkX is available, its ``degree_centrality``
        function is used (which produces values normalised by ``1/(n-1)``).  If
        NetworkX is not available, a simple degree‑based computation is used.
        Finally, the resulting values are rescaled by a factor of ``n/sum`` to
        ensure that the sum of values equals ``n``.  This rescaling makes
        reasoning graphs with different numbers of nodes comparable and
        satisfies the expectation that the distribution integrates to the
        total number of nodes.
        """
        G = self.graph
        n = G.number_of_nodes()
        # No nodes → return empty mapping
        if n == 0:
            return {}
        # Attempt to compute using NetworkX if available
        try:
            dc = nx.degree_centrality(G)
        except Exception:
            # Fallback to manual computation: degree divided by (n-1) where
            # ``n-1`` is the maximum possible degree in a directed graph.
            denom = (n - 1) if n > 1 else 1
            dc = {node: (G.degree(node) / denom) for node in G.nodes()}
        total = float(sum(dc.values()))
        # If the total is extremely small (no edges), assign 1.0 uniformly
        if total <= 1e-12:
            return {node: 1.0 for node in G.nodes()}
        # Rescale so that sum of values equals n
        scale = n / total
        return {node: val * scale for node, val in dc.items()}