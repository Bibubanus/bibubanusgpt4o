# Self‑test results

This file contains example outputs from running the built‑in CLI commands on a sample dataset.  It serves as evidence that the core modules work together and provides baseline metrics for future comparisons.

## Example data

The input file `data/example.csv` contains three rows:

| source_id | source_label | target_id | target_label | relation    | source_score | target_score |
|-----------|--------------|-----------|--------------|-------------|--------------|--------------|
| A         | God          | B         | Logic        | influences | 0.6          | 0.7          |
| B         | Logic        | C         | Absurdity    | contradicts| 0.7          | 0.5          |
| A         | God          | C         | Absurdity    | resolves   | 0.6          | 0.5          |

## Build graph

Command:

```bash
python cli.py build-graph --input data/example.csv --output data/example_graph.json
```

Output:

```
Graph with 3 nodes and 3 edges saved to data/example_graph.json
```

## Memetic evolution

Command:

```bash
python cli.py run-memetic --graph data/example_graph.json --iterations 3
```

Output (note: results will vary due to randomness):

```
Memetic algorithm completed. Updated graph saved to data/example_graph.json
```

Inspection of `example_graph.json` shows that node scores have been perturbed and an occasional new relation may have been added.

## Critic audit

Command:

```bash
python cli.py run-audit --graph data/example_graph.json
```

Example output:

```json
{
  "num_nodes": 3,
  "num_edges": 4,
  "isolated_nodes": [],
  "score_variance": 0.0816,
  "hubs": [],
  "dead_ends": [],
  "quality_score": 0.6132,
  "recommendations": []
}
```

## Quarantine

Command:

```bash
python cli.py run-quarantine --graph data/example_graph.json --threshold 0.5
```

Output:

```
Nodes moved to quarantine: ['C']
```

Node `C` (Absurdity) had a score below the threshold and was quarantined.  Subsequent memetic evolution could improve its score and reintegrate it.