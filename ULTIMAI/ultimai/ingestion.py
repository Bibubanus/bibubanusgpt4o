"""Data ingestion utilities for ULTIMAI.

This module provides helpers for loading reasoning data into a
ReasoningGraph.  Seeds can be supplied as JSON (see data/seeds.json) or
CSV.  The ingestion functions return a ReasoningGraph instance.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from .graph import ReasoningGraph, NodeData


def ingest_json(path: str) -> ReasoningGraph:
    """Ingest seed data from a JSON file.

    The JSON file should contain a list of objects with keys:
    source_id, source_label, target_id, target_label, relation,
    source_score, target_score.
    """
    rg = ReasoningGraph()
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for row in data:
        src = str(row.get("source_id"))
        dst = str(row.get("target_id"))
        if not rg.graph.has_node(src):
            rg.add_node(src, NodeData(
                label=row.get("source_label", src),
                score=float(row.get("source_score")) if row.get("source_score") is not None else None,
                metadata={},
            ))
        if not rg.graph.has_node(dst):
            rg.add_node(dst, NodeData(
                label=row.get("target_label", dst),
                score=float(row.get("target_score")) if row.get("target_score") is not None else None,
                metadata={},
            ))
        rg.add_edge(src, dst, relation=row.get("relation", "influences"), weight=float(row.get("weight", 1.0)))
    return rg


def ingest(path: str) -> ReasoningGraph:
    """Ingest data from either a JSON or CSV file."""
    ext = Path(path).suffix.lower()
    rg = ReasoningGraph()
    if ext == ".json":
        return ingest_json(path)
    elif ext == ".csv":
        rg.from_csv(Path(path))
        return rg
    else:
        raise ValueError(f"Unsupported input format: {ext}")