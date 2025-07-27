"""Tests for the stress test module."""

from ultimai.stress_test import run_stress_test


def test_stress_metrics() -> None:
    metrics = run_stress_test(iterations=2, threshold=0.3)
    # Ensure expected keys exist
    assert set(metrics.keys()) == {'num_nodes', 'num_edges', 'quarantined', 'reintegrated'}
    assert metrics['num_nodes'] == 3
    assert metrics['num_edges'] >= 2
    assert metrics['quarantined'] >= 0
    assert metrics['reintegrated'] >= 0