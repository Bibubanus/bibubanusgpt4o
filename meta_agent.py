"""Meta‑agent orchestrating reasoning processes.

The MetaAgent manages the lifecycle of reasoning: ingestion of new data,
construction of the reasoning graph, execution of memetic evolution,
quarantine and critic audits, and integration of external knowledge.

This class is intended as a high‑level entry point for workflows.  It
coordinates lower‑level modules but does not enforce a fixed schedule; users
can customise the order and parameters of operations.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .graph_manager import ReasoningGraph
from .memetic_algorithm import MemeticEngine
from .quarantine import Quarantine
from .critic import Critic


@dataclass
class MetaConfig:
    quarantine_threshold: float = 0.35
    memetic_iterations: int = 10
    reintegrate_threshold: float = 0.6


class MetaAgent:
    def __init__(self, config: Optional[MetaConfig] = None) -> None:
        self.config = config or MetaConfig()
        self.rg = ReasoningGraph()
        self.engine: Optional[MemeticEngine] = None
        self.quarantine = Quarantine(self.config.quarantine_threshold)
        self.critic = Critic()

    def load_data(self, csv_path: Optional[str] = None, json_path: Optional[str] = None) -> None:
        """Load reasoning data into the graph from CSV or JSON."""
        if csv_path:
            self.rg.from_csv(Path(csv_path))
        elif json_path:
            self.rg.from_json(Path(json_path))

    def build_graph(self) -> None:
        """Initialize memetic engine after graph is loaded."""
        self.engine = MemeticEngine(self.rg)

    def run_memetic(self) -> None:
        if not self.engine:
            self.build_graph()
        assert self.engine is not None
        self.engine.run(self.config.memetic_iterations)

    def run_quarantine(self) -> None:
        quarantined = self.quarantine.evaluate(self.rg)
        if quarantined:
            print(f"[MetaAgent] Quarantined {len(quarantined)} nodes: {quarantined}")

    def reintegrate_quarantine(self) -> None:
        reintegrated = self.quarantine.reintegrate(self.rg, self.config.reintegrate_threshold)
        if reintegrated:
            print(f"[MetaAgent] Reintegrated nodes: {reintegrated}")

    def audit(self) -> None:
        report = self.critic.audit_graph(self.rg)
        print("[MetaAgent] Audit report:\n", report)

    def save_graph(self, path: str) -> None:
        self.rg.save(path)

    def full_cycle(self, csv_path: Optional[str] = None, json_path: Optional[str] = None, save_path: Optional[str] = None) -> None:
        """Run a full reasoning cycle: load data, memetic evolution, quarantine, audit and save."""
        self.load_data(csv_path, json_path)
        self.build_graph()
        self.run_memetic()
        self.run_quarantine()
        self.reintegrate_quarantine()
        self.audit()
        if save_path:
            self.save_graph(save_path)