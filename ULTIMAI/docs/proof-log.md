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