# ULTIMAI Reasoning Infrastructure

<!-- CI and Pages badges -->

![CI](https://github.com/Bibubanus/bibubanusgpt4o/actions/workflows/ci.yml/badge.svg)
![Pages](https://github.com/Bibubanus/bibubanusgpt4o/actions/workflows/pages.yml/badge.svg)


This repository contains a simplified reasoning infrastructure inspired by the ULTIMAI project.  It provides a modular graph representation, quarantine and memetic evolution modules, an orchestrator for meta‑synthesis, and scripts for generating graphs and audit reports.  The code is intentionally lightweight and avoids hard dependencies so that it can run in restricted environments (e.g. without internet access).

## Quick start

1. **Install system requirements:** You need Python 3.8 or higher.  Optional packages such as Graphviz and matplotlib can be installed for improved graph visualisation.
2. **Run tests:**

```bash
make test
```

3. **Generate a graph:**

```bash
make build_graph
```

4. **Generate an audit report:**

```bash
make report
```

5. See `docs/` for architecture overview, FAQs and logs.

## Docker support

The project can be run in Docker containers for isolated and reproducible environments.

### Build and run with Docker

1. **Build the Docker image:**

```bash
docker build -t ultimai:latest .
```

2. **Run tests in Docker:**

```bash
docker run --rm ultimai:latest
```

3. **Generate graph in Docker:**

```bash
docker run --rm -v $(pwd)/build:/app/build -v $(pwd)/data:/app/data ultimai:latest python scripts/generate_graph.py --input data/seeds.json --output build/graph/graph.json
```

4. **Generate report in Docker:**

```bash
docker run --rm -v $(pwd)/build:/app/build ultimai:latest python scripts/dump_report.py --graph build/graph/graph.json --output build/report/report.md
```

### Using Docker Compose

Docker Compose provides a simpler way to run multiple services:

1. **Run tests:**

```bash
docker compose run --rm ultimai
```

2. **Generate graph:**

```bash
docker compose run --rm generate-graph
```

3. **Generate report:**

```bash
docker compose run --rm generate-report
```

4. **Build all services:**

```bash
docker compose build
```

## Repository structure

```
ULTIMAI/
├── pyproject.toml          # Packaging configuration
├── requirements.txt        # Optional dependencies (mostly empty)
├── Makefile                # Common tasks (tests, build, report)
├── README.md               # This file
├── SECURITY.md             # Security policy
├── CONTRIBUTING.md         # Contribution guidelines
├── CODEOWNERS              # Ownership information
├── ultimai/                # Python package
│   ├── __init__.py
│   ├── graph.py            # Reasoning graph representation
│   ├── quarantine.py       # Quarantine low‑quality nodes
│   ├── reasoning_modulator.py # Memetic algorithm
│   ├── meta_synthesizer.py # Orchestrator combining modules
│   ├── ingestion.py        # Data ingestion helpers
│   ├── stress_test.py      # Stress test runner
│   └── critic.py           # Audit and quality metrics
├── scripts/                # CLI scripts
│   ├── generate_graph.py   # Build a graph from seeds
│   ├── dump_report.py      # Dump an audit report
│   └── verify_integrity.sh # Run tests for verification
├── tests/                  # Unit tests and test runner
│   ├── run_tests.py
│   ├── test_graph.py
│   ├── test_quarantine.py
│   ├── test_meta.py
│   ├── test_modulator.py
│   └── test_stress.py
├── data/                   # Example data and configuration
│   ├── seeds.json
│   └── config.yaml
├── docs/                   # Documentation and logs
│   ├── index.md
│   ├── architecture.md
│   ├── faq.md
│   ├── risks.md
│   ├── proof-log.md
│   ├── cross-reference-log.md
│   └── troubleshooting.md
└── .github/
    └── workflows/
        ├── ci.yml          # Continuous integration pipeline
        └── pages.yml       # GitHub Pages deployment
```

### Local development

The project does not depend on any external Python packages.  You can install optional packages such as `graphviz` and `matplotlib` to enable graph rendering.  See the `Makefile` for useful commands.  Contributions are welcome; see `CONTRIBUTING.md` for details.