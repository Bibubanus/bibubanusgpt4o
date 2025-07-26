# ULTIMAI Reasoning Infrastructure

This repository contains an improved reasoning–infrastructure for the ULTIMAI project.  It is a modular, multi‑agent system designed to ingest heterogeneous knowledge artifacts, build dynamic reasoning graphs, run memetic algorithms for idea evolution, quarantine low‑quality branches, perform critic audits and meta–synthesis, and expose the resulting knowledge through a simple API and front‑end.

## Repository structure

```
agent_research2/
├── README.md                # High‑level description and usage instructions
├── requirements.txt         # Python dependencies
├── cli.py                   # Command line interface for running tasks
├── ultimai/                 # Python package containing core modules
│   ├── __init__.py
│   ├── graph_manager.py     # Build and manipulate reasoning graphs
│   ├── memetic_algorithm.py # Memetic algorithm for evolving reasoning patterns
│   ├── quarantine.py        # Isolate and reintegrate problematic nodes
│   ├── critic.py            # Audit reasoning steps and detect blind spots
│   ├── meta_agent.py        # Orchestrator combining modules and running pipelines
│   ├── integration.py       # Hooks to external data sources (placeholders)
│   ├── explainability.py    # Knowledge‑graph and explanation utilities
│   └── utils.py             # Shared utilities
├── analysis/
│   ├── cross_reference_log.md  # Mapping of archive files to modules/steps
│   ├── proof_log.md            # Evidence for architectural choices (citations)
│   └── self_test_results.md    # Results of self‑tests and audits
├── docs/
│   ├── architecture.md         # Detailed architecture explanation
│   ├── deployment.md           # Step‑by‑step deployment and CI/CD instructions
│   └── faq.md                  # Frequently asked questions
├── scripts/
│   ├── build_graph.py          # Example script to construct a reasoning graph from CSV/MD files
│   ├── visualize_graph.py      # Render the reasoning graph to an image (requires Graphviz)
│   └── stress_test.py          # Memetic stress‑tests and failure mode exploration
└── .github/
    └── workflows/
        ├── ci.yml              # Linting, unit tests and build checks
        └── pages.yml           # Deployment to GitHub Pages (static docs)
```

### Quick start

1. **Install dependencies**: `pip install -r requirements.txt`.
2. **Run a basic graph build**: `python scripts/build_graph.py --input data/combined.csv --output graph.json`.
3. **Visualize the graph**: `python scripts/visualize_graph.py --graph graph.json --output graph.png`.
4. **Perform a memetic stress test**: `python scripts/stress_test.py`.
5. See [`docs/deployment.md`](docs/deployment.md) for instructions on configuring CI/CD and GitHub Pages.

## Motivation and design

This infrastructure is inspired by the ideas, experiments and discussions contained in the ULTIMAI reasoning archives.  It draws on modern best‑practice frameworks (e.g. LangGraph, AutoGen, GraphAgent‑Reasoner, KG4XAI and memetic algorithms) and combines them into a cohesive architecture with modular agents, a dynamic reasoning graph, integrated knowledge‑graph semantics and robust auditing.

The system is designed to be extensible: new data sources, agents and analysis modules can be plugged in without disrupting existing functionality.  Care has been taken to minimise external dependencies and to provide clear documentation, both for users who want to run the system and for developers who wish to extend it.

Please see the `analysis` and `docs` directories for detailed cross‑reference logs, proof logs, design diagrams and FAQs.