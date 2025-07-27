"""MetaSynthesizer orchestrates the reasoning cycle.

The MetaSynthesizer manages the pipeline: ingesting data into a
reasoning graph, running memetic evolution, applying quarantine rules,
conducting an audit via the critic and saving results.  Configurable
parameters are provided through a simple configuration dictionary.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .graph import ReasoningGraph
from .reasoning_modulator import MemeticEngine
from .quarantine import Quarantine
from .critic import Critic


@dataclass
class MetaConfig:
    memetic_iterations: int = 10
    quarantine_threshold: float = 0.35
    reintegrate_threshold: float = 0.6


class MetaSynthesizer:
    def __init__(self, config: Optional[MetaConfig] = None) -> None:
        self.config = config or MetaConfig()
        self.graph = ReasoningGraph()
        self.engine: Optional[MemeticEngine] = None
        self.quarantine = Quarantine(self.config.quarantine_threshold)
        self.critic = Critic()

    def load_data(self, csv_path: Optional[str] = None, json_path: Optional[str] = None) -> None:
        if csv_path:
            self.graph.from_csv(Path(csv_path))
        elif json_path:
            self.graph.from_json(Path(json_path))

    def build_engine(self) -> None:
        self.engine = MemeticEngine(self.graph)

    def run_memetic(self) -> None:
        if self.engine is None:
            self.build_engine()
        assert self.engine is not None
        self.engine.run(self.config.memetic_iterations)

    def run_quarantine(self) -> None:
        self.quarantine.evaluate(self.graph)
        self.quarantine.reintegrate(self.graph, self.config.reintegrate_threshold)

    def audit(self) -> dict:
        return self.critic.audit_graph(self.graph)

    def save_graph(self, path: str) -> None:
        self.graph.save(Path(path))

    def full_cycle(self, csv_path: Optional[str] = None, json_path: Optional[str] = None, save_path: Optional[str] = None) -> dict:
        self.load_data(csv_path, json_path)
        self.build_engine()
        self.run_memetic()
        self.run_quarantine()
        report = self.audit()
        if save_path:
            self.save_graph(save_path)
        return report