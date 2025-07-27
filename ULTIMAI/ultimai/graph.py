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
        return nx.degree_centrality(self.graph)

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