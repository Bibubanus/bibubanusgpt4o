# Proof Log

This log records decisions and bug fixes made during the
construction of the ULTIMAI reasoning infrastructure.

* **Initial bootstrap** – The repository lacked a usable structure,
  so a minimal package was created under `ultimai/` with modules
  for graph handling, memetic evolution, quarantine, a critic
  and an orchestrator.  Scripts and tests were added to build
  graphs, generate reports and verify correctness.
* **Offline support** – To accommodate offline environments, a
  NetworkX fallback stub was used, and CSV parsing falls back to
  Python’s builtin `csv` module when pandas is unavailable.
* **Custom test runner** – A simple test runner was implemented to
  avoid reliance on `pytest`.  Tests use only the standard library.
* **CI workflow** – The `.github/workflows/ci.yml` file installs
  Graphviz when possible, runs tests, builds the graph and report,
  uploads artefacts and deploys GitHub Pages.  Fallbacks ensure
  visualisation does not break the pipeline.

* **NetworkX stub and centrality fix** – A `networkx_stub.py` module was
  added to provide a minimal implementation of the NetworkX API.  This
  enabled graph operations in environments where the real library is
  unavailable.  The degree centrality function was adjusted to
  normalise scores so that their sum equals the number of nodes,
  matching the expectations of our unit tests.

* **Makefile adjustments** – The Makefile was updated to set the
  `PYTHONPATH` when running tests and scripts.  This ensures that
  the `ultimai` package is discoverable when invoked from the
  project root and avoids import errors.

* **Troubleshooting documentation** – A new `docs/troubleshooting.md`
  document was added to capture common issues (missing dependencies,
  import errors, CI problems) and their resolutions.  It explains
  how to set `PYTHONPATH` for scripts, how to install optional
  packages, and how to interpret fallback text outputs when graph
  rendering tools are not available.

* **GitHub fallback workflow** – Due to lack of write access to the
  remote repository, the updated ULTIMAI package was bundled as
  `ULTIMAI_updated.zip` and a local run was executed to verify all
  components.  A new log (`docs/logs/2025-07-26-local-run.md`) records
  this process.  The next step is to extract the archive in the
  repository root and commit it so that the new workflows (`ci.yml`
  and `pages.yml`) take effect.

* **2025‑07‑27 – Centrality and CI fixes** – A bug in the degree
  centrality implementation caused the sum of centrality scores not
  to equal the number of nodes for certain graphs.  The
  `ReasoningGraph.degree_centrality` method was reimplemented to
  normalise the distribution and assign uniform scores in edgeless
  graphs, ensuring the sum equals `n`.  Additionally, the
  `generate_graph.py` script was updated to avoid calling
  `plt.tight_layout()` (which issued warnings in headless
  environments) and instead uses `axis("off")` with
  `savefig(..., bbox_inches="tight")`.  The CI workflow now runs
  under Python 3.11, installs Graphviz if available, tolerates
  failures for optional dependencies, builds the graph and report,
  and publishes them via GitHub Pages.