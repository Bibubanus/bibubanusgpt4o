# Deployment and CI/CD

This document provides step‑by‑step instructions for setting up the ULTIMAI reasoning infrastructure, configuring continuous integration and deploying artefacts to GitHub Pages.  Because the GitHub API available through connectors does not permit writing to repositories, these steps must be executed manually by a repository owner or collaborator.

## 1. Local setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/bibubanusgpt4o.git
   cd bibubanusgpt4o
   ```

2. **Copy the contents** of the `agent_research2` directory from this analysis environment into the cloned repository.  Ensure that the directory structure (`ultimai`, `docs`, `analysis`, `.github`) is preserved.

3. **Install dependencies** (preferably in a virtual environment):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Run tests** to verify that the code executes:
   ```bash
   python cli.py build-graph --input data/example.csv --output graph.json
   python cli.py run-memetic --graph graph.json --iterations 5
   python cli.py run-audit --graph graph.json
   ```


## 2. CI/CD configuration

### GitHub Actions

Two workflows are provided under `.github/workflows`:

* **ci.yml**: Runs on every push.  It checks out the repository, installs Python, installs dependencies, runs flake8/black linting, executes unit tests (if present) and generates the latest reasoning graph.  Adjust this file to suit your testing strategy.

* **pages.yml**: Builds static documentation and deploys it to GitHub Pages.  It uses the `actions/upload-pages-artifact` and `actions/deploy-pages` actions.  Before using this, enable GitHub Pages for your repository and specify the deployment branch (`gh-pages`).


### Setting up GitHub Pages

1. In your GitHub repository settings, enable **GitHub Pages** and select the `gh-pages` branch as the source.  Choose the root directory or `/docs` as appropriate.
2. The `pages.yml` workflow will build the documentation (e.g. converting Markdown to HTML) and publish it automatically.  Adjust the `deploy_dir` in the workflow file if you use a different build process.


## 3. Data ingestion

Place your aggregated reasoning data (CSV or JSON) in a directory, e.g. `data/combined.csv`.  Ensure that the columns match those expected by `ReasoningGraph.from_csv()`.


## 4. Running the pipeline

Once the environment is set up and data is prepared:

1. **Initial graph build**:
   ```bash
   python cli.py build-graph --input data/combined.csv --output data/reasoning_graph.json
   ```

2. **Memetic evolution**:
   ```bash
   python cli.py run-memetic --graph data/reasoning_graph.json --iterations 10
   ```

3. **Quarantine and audit**:
   ```bash
   python cli.py run-quarantine --graph data/reasoning_graph.json --threshold 0.35
   python cli.py run-audit --graph data/reasoning_graph.json
   ```

4. **Visualisation** (optional):
   ```bash
   python scripts/visualize_graph.py --graph data/reasoning_graph.json --output assets/graph.png
   ```

Commit and push these changes back to GitHub to keep your repository up to date.  The CI pipeline will validate and publish updates automatically.


## 5. Security considerations

* **Code security**: Use code scanning tools (e.g. GitHub's CodeQL) to detect vulnerabilities.  Always review contributions.
* **Data privacy**: Avoid committing sensitive data.  If you integrate proprietary APIs, store keys in GitHub Secrets and reference them in workflows.
* **Memetic defence**: Implement rate limiting and input validation on any public APIs to mitigate injection attacks.  Use the `critic` and `quarantine` modules to guard against memetic parasites (patterns designed to exploit reasoning loops).


## 6. Monitoring and maintenance

* Schedule regular runs of the memetic algorithm and audits via GitHub Actions (e.g. daily or weekly cron triggers).
* Track the size and complexity of the reasoning graph.  If the graph grows too large, consider sharding it into domains or time windows.
* Use the `analysis` directory to log results of self tests and audits.  Commit updated `cross_reference_log.md` and `proof_log.md` to maintain transparency.
