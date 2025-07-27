"""Tests for the MetaSynthesizer orchestrator."""

from pathlib import Path
import json

from ultimai.meta_synthesizer import MetaSynthesizer, MetaConfig
from ultimai.graph import ReasoningGraph


def test_full_cycle(tmp_path: Path) -> None:
    # prepare a small CSV file
    csv_path = tmp_path / 'input.csv'
    csv_path.write_text(
        "source_id,source_label,target_id,target_label,relation,source_score,target_score\n"
        "A,Alpha,B,Beta,influences,0.6,0.7\n"
        "B,Beta,C,Gamma,contradicts,0.7,0.5\n"
        "A,Alpha,C,Gamma,resolves,0.6,0.5\n"
    )
    json_path = tmp_path / 'graph.json'
    synth = MetaSynthesizer(config=MetaConfig(memetic_iterations=2, quarantine_threshold=0.3, reintegrate_threshold=0.4))
    report = synth.full_cycle(csv_path=str(csv_path), save_path=str(json_path))
    # ensure the graph file was saved
    assert json_path.exists()
    data = json.loads(json_path.read_text())
    assert 'nodes' in data and 'links' in data
    # report should contain keys
    assert 'num_nodes' in report and 'quality_score' in report