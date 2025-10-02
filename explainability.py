"""Explainability utilities.

This module provides helper functions to extract human‑readable explanations from
the reasoning graph.  Functions include retrieving justification paths,
producing natural language summaries and exporting knowledge graphs.
"""

from __future__ import annotations

from typing import List, Dict, Any, Optional
import networkx as nx

from .graph_manager import ReasoningGraph


def get_justification_path(rg: ReasoningGraph, start: str, end: str) -> List[str]:
    """Return one of the shortest paths (list of nodes) between two concepts."""
    try:
        path = nx.shortest_path(rg.graph, start, end)
        return path
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return []


def summarise_concept(rg: ReasoningGraph, node_id: str) -> str:
    """Generate a simple textual summary of a concept node."""
    node = rg.graph.nodes.get(node_id)
    if not node:
        return f"Concept '{node_id}' not found."
    label = node.get('label', node_id)
    source = node.get('source')
    score = node.get('score')
    parts = [f"**{label}**"]
    if source:
        parts.append(f"(source: {source})")
    if score is not None:
        parts.append(f"score: {score:.2f}")
    return ' '.join(parts)


def export_as_kg(rg: ReasoningGraph) -> Dict[str, Any]:
    """Export the reasoning graph in a simple knowledge‑graph serialisation.

    Returns a dict with lists of `entities` and `relations`.  Each entity
    contains its id, label and attributes.  Each relation contains source,
    target and relation type.
    """
    entities = []
    for node_id, attrs in rg.graph.nodes(data=True):
        entities.append({
            'id': node_id,
            'label': attrs.get('label', node_id),
            'type': attrs.get('type', 'concept'),
            'score': attrs.get('score'),
            'source': attrs.get('source'),
            'metadata': attrs.get('metadata', {})
        })
    relations = []
    for src, dst, attrs in rg.graph.edges(data=True):
        relations.append({
            'source': src,
            'target': dst,
            'relation': attrs.get('relation', 'influences'),
            'weight': attrs.get('weight', 1.0)
        })
    return {'entities': entities, 'relations': relations}