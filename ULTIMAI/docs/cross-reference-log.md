# Cross‑reference Log

This log maps elements of the repository to their origin and purpose.

| Origin | Module / Script | Purpose |
|---|---|---|
| Seed data (`data/seeds.json`) | `ultimai/ingestion.py` | Defines the initial concepts and relations.  Ingested into the reasoning graph. |
| Memetic algorithm | `ultimai/reasoning_modulator.py` | Implements a simple memetic engine inspired by the ULTIMAI archives’ discussion of idea evolution. |
| Quarantine design | `ultimai/quarantine.py` | Isolates nodes below a threshold, reflecting concerns about parasitic memetic branches in the archives. |
| Critic metrics | `ultimai/critic.py` | Computes quality and identifies blind spots.  Based on analyses from previous prototypes. |
| Orchestration | `ultimai/meta_synthesizer.py` | Combines ingestion, evolution, quarantine and auditing into a single pipeline. |
| Stress test | `ultimai/stress_test.py` | Provides a reproducible way to stress the memetic engine and quarantine logic. |
| NetworkX fallback | `ultimai/networkx_stub.py` | Provides a minimal in‑house implementation of the NetworkX API when the real library is unavailable.  Ensures graph operations work in offline CI environments. |
| Custom test runner | `tests/run_tests.py` | A lightweight runner that discovers and executes test functions without relying on external testing frameworks. |
| CI workflow | `.github/workflows/ci.yml` | Automates testing, graph and report generation, artefact upload and prepares data for GitHub Pages. |
| Pages workflow | `.github/workflows/pages.yml` | Deploys the generated graph and report as a static site via GitHub Pages. |
| Troubleshooting guide | `docs/troubleshooting.md` | Documents common issues (missing dependencies, import errors, CI failures) and how to resolve them. |
| Graph generation | `scripts/generate_graph.py` | Reads seeds and produces a graph and image for the CI pipeline. |
| Report generation | `scripts/dump_report.py` | Writes a markdown audit report summarising graph metrics. |