"""Reasoning graph management for ULTIMAI.

The reasoning graph is represented using NetworkX.  Each node corresponds to a
concept, idea or artefact extracted from the ULTIMAI archives, logs or external
research.  Each edge represents a relationship (causal, derivation, conflict,
analogy, etc.).

Nodes have attributes:
  - `label`: human‑readable name or description.
  - `type`: category (e.g. 'concept', 'code', 'pattern', 'agent').
  - `source`: origin of the idea (file name, research article, etc.).
  - `score`: importance or confidence (optional).
  - `metadata`: arbitrary dictionary for extensions.

Edges have attributes:
  - `relation`: type of relationship (e.g. 'influences', 'contradicts', 'extends').
  - `weight`: numeric weight (default=1).

This module provides methods to construct graphs from tabular data (CSV), JSON,
to save/load graphs, and to compute basic metrics.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from typing import Any, Dict, Iterable, List, Optional
from pathlib import Path

import pandas as pd
import networkx as nx


@dataclass
class NodeData:
    label: str
    type: str = "concept"
    source: Optional[str] = None
    score: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None


class ReasoningGraph:
    """Container for a reasoning graph."""

    def __init__(self) -> None:
        self.graph: nx.DiGraph = nx.DiGraph()

    def add_node(self, node_id: str, data: NodeData) -> None:
        self.graph.add_node(node_id, **asdict(data))

    def add_edge(self, src: str, dst: str, relation: str = "influences", weight: float = 1.0) -> None:
        self.graph.add_edge(src, dst, relation=relation, weight=weight)

    def from_csv(self, path: Path) -> None:
        """Load nodes and edges from a CSV file.

        The CSV must have columns: 'source_id', 'target_id', 'source_label', 'target_label',
        'relation', 'source_type', 'target_type', 'source_score', 'target_score', 'source_file',
        'target_file'.  Missing columns are allowed and default values will be used.
        """
        df = pd.read_csv(path)
        for _, row in df.iterrows():
            src = str(row['source_id']) if 'source_id' in row else str(row['source_label'])
            dst = str(row['target_id']) if 'target_id' in row else str(row['target_label'])
            # Create source node
            if not self.graph.has_node(src):
                self.add_node(src, NodeData(
                    label=row.get('source_label', src),
                    type=row.get('source_type', 'concept'),
                    source=row.get('source_file'),
                    score=row.get('source_score'),
                    metadata={}
                ))
            # Create target node
            if not self.graph.has_node(dst):
                self.add_node(dst, NodeData(
                    label=row.get('target_label', dst),
                    type=row.get('target_type', 'concept'),
                    source=row.get('target_file'),
                    score=row.get('target_score'),
                    metadata={}
                ))
            # Add edge
            self.add_edge(src, dst, relation=row.get('relation', 'influences'), weight=row.get('weight', 1.0))

    def from_json(self, path: Path) -> None:
        """Load graph from a JSON file previously saved by `save`."""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        g = nx.node_link_graph(data)
        self.graph = g  # type: ignore

    def save(self, path: str | Path) -> None:
        """Save the graph to a JSON file using node‑link format."""
        data = nx.node_link_data(self.graph)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self, path: str | Path) -> None:
        """Alias for from_json for backwards compatibility."""
        self.from_json(Path(path))

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
        """Return a subgraph containing only the specified nodes."""
        sg = ReasoningGraph()
        sg.graph = self.graph.subgraph(nodes).copy()
        return sg


    # Example convenience methods
    def add_concept(self, concept: str, description: str, source: Optional[str] = None, score: Optional[float] = None) -> None:
        """Add a high‑level concept node."""
        self.add_node(concept, NodeData(label=description, type='concept', source=source, score=score, metadata={}))

    def link_concepts(self, from_concept: str, to_concept: str, relation: str = 'influences', weight: float = 1.0) -> None:
        """Link two existing concepts."""
        if from_concept not in self.graph or to_concept not in self.graph:
            raise ValueError("Both concepts must be added before linking")
        self.add_edge(from_concept, to_concept, relation, weight)