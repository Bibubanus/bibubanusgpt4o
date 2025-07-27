# Frequently Asked Questions

**Why does the project avoid external dependencies?**

The environment in which ULTIMAI is developed may lack internet
access, making it difficult to install packages from PyPI.  To
ensure reproducibility, the core functionality relies solely on
Python’s standard library.  Optional packages such as NetworkX,
pandas, matplotlib or pygraphviz can be installed to enhance
performance and visualisation but are not required.

**How do I visualise the reasoning graph?**

The `scripts/generate_graph.py` script will attempt to render the
graph using pygraphviz (Graphviz), falling back to matplotlib and
finally to a textual representation.  You can install these
packages if your environment allows (`sudo apt-get install
graphviz libgraphviz-dev` and `pip install matplotlib pygraphviz`).

**How do I contribute tests?**

Add new test files under `tests/` with names starting with
`test_`.  Tests should be functions prefixed with `test_` and may
optionally accept a single argument `tmp_path` which will be
supplied with a temporary directory by the test runner.

**How do I deploy GitHub Pages?**

The CI workflow builds the graph and report and deploys them via
GitHub Pages.  See `.github/workflows/ci.yml` and
`.github/workflows/pages.yml` for details.