"""Top‑level package for ULTIMAI reasoning infrastructure.

This package aggregates the core modules that implement the reasoning graph,
memetic evolution, quarantine logic, critic audits, meta agent orchestration
and integration hooks.  See the README for usage instructions.
"""

from .graph_manager import ReasoningGraph  # noqa: F401
from .memetic_algorithm import MemeticEngine  # noqa: F401
from .critic import Critic  # noqa: F401
from .quarantine import Quarantine  # noqa: F401
from .meta_agent import MetaAgent  # noqa: F401