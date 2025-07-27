# Architecture

The ULTIMAI reasoning infrastructure is composed of several modular
components:

* **Reasoning graph (`ultimai/graph.py`)** – a directed graph of
  concepts and relationships.  Each node carries a label, type,
  source, optional score and metadata.  The graph can be loaded from
  CSV or JSON and saved in node‑link format.
* **Memetic engine (`ultimai/reasoning_modulator.py`)** – implements a
  simple memetic algorithm that mutates node scores and occasionally
  introduces new relations.  It evaluates candidates via the critic
  and keeps improvements.
* **Quarantine (`ultimai/quarantine.py`)** – isolates nodes whose
  score falls below a threshold and reintegrates them when their
  score improves.
* **Critic (`ultimai/critic.py`)** – computes a quality score based
  on edge density, mean node score and inverse centralisation.  It
  reports isolated nodes, hubs and dead ends.
* **MetaSynthesizer (`ultimai/meta_synthesizer.py`)** – orchestrates
  the full reasoning cycle: ingestion, memetic evolution, quarantine,
  auditing and saving results.

The `scripts/` directory contains utilities to build graphs from seed
data and to dump audit reports.  Tests in `tests/` verify the
functionality of each component.  See `docs/risks.md` and
`docs/troubleshooting.md` for known limitations and workarounds.