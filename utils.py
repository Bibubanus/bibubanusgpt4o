"""Utility functions for the ULTIMAI reasoning infrastructure."""

from typing import List, Iterable
import numpy as np

def normalize_scores(scores: Iterable[float]) -> List[float]:
    """Normalize a list of scores to sum to 1, avoiding division by zero."""
    scores = np.array(list(scores), dtype=float)
    total = scores.sum()
    if total == 0:
        # Avoid division by zero by returning equal weights
        return [1.0 / len(scores)] * len(scores)
    return (scores / total).tolist()


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Compute cosine similarity between two vectors."""
    denom = (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    if denom == 0:
        return 0.0
    return float(np.dot(vec1, vec2) / denom)


def clamp(value: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """Clamp a value to a given range."""
    return max(min_val, min(value, max_val))