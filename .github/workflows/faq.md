# FAQ

This FAQ addresses common questions about the ULTIMAI reasoning infrastructure.

### Q: How does the reasoning graph differ from a standard knowledge graph?

The reasoning graph focuses on the *process* of reasoning rather than static facts.  Nodes capture concepts, code snippets, memetic fragments and agents; edges represent causal, supportive or conflicting relationships.  It is dynamic and evolves through memetic algorithms and audits, whereas a conventional knowledge graph tends to be more static and descriptive.

### Q: Where do the initial nodes and edges come from?

The initial data is extracted from the ULTIMAI archives (text files, logs, markdown documents, CSV tables) and structured into a tabular form with source and target concepts.  You can append external research or reasoning logs by adding rows to the CSV.  See `scripts/build_graph.py` for an example.

### Q: What is the quarantine and why do I need it?

Quarantine isolates reasoning nodes that fall below a confidence threshold or exhibit high variance.  This prevents low‑quality or potentially harmful patterns from propagating.  Quarantined nodes can be reviewed and reintegrated when their scores improve, maintaining the health of the reasoning ecosystem.

### Q: How do I integrate external APIs?

The `integration.py` module defines a `DataSource` class.  To integrate an API, subclass `DataSource`, implement the `fetch()` method to return a list of results for a query, and register your class in `get_available_sources()`.  For security, store API keys in environment variables or GitHub Secrets and load them at runtime.

### Q: Can I visualise the reasoning graph?

Yes.  Use `scripts/visualize_graph.py` to render the graph to an image using Graphviz.  For more interactive exploration, you can build a front‑end with D3.js or React and consume the exported JSON/knowledge graph.

### Q: How is this system aligned with multi‑agent best practices?

The design emphasises modularity, specialisation and explainability.  Each component (memetic engine, critic, quarantine) can be considered a micro‑agent with its own task.  This follows recommendations from contemporary multi‑agent frameworks【906438729630143†L116-L139】.  You can further decompose the system into sub‑agents operating on subgraphs or specific disciplines.

### Q: What if the memetic algorithm behaves unpredictably?

Memetic evolution introduces randomness, but you can control its behaviour by adjusting the number of iterations, the mutation parameters in `MemeticEngine._mutate()` and the local search depth.  Always run the critic and quarantine after memetic evolution to detect anomalies and regressions.

### Q: How do I update the reasoning graph with new data?

1. Append new rows to your CSV or produce an updated JSON describing the new nodes and relationships.
2. Run `python cli.py build-graph` to rebuild or merge the graph.
3. Run `python cli.py run-memetic` and `python cli.py run-quarantine` to evolve and clean the graph.
4. Commit and push the updated graph to version control.

### Q: Where can I read about the theories behind this system?

See the `analysis/proof_log.md` file, which references the ULTIMAI archives and external research papers.  Key topics include multi‑agent reasoning frameworks【166755538859472†L20-L37】, knowledge graph explainability【928960283267357†L56-L114】【850674227268130†L45-L75】, memetic algorithms【230422289242979†L41-L87】 and systemic self‑testing.