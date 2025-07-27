"""Utility functions for the ULTIMAI project."""

from __future__ import annotations

def clamp(value: float, lower: float, upper: float) -> float:
    """Clamp a value between a lower and upper bound."""
    return max(lower, min(upper, value))