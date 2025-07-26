# Architecture of the ULTIMAI Reasoning Infrastructure

The ULTIMAI reasoning infrastructure is built around a **dynamic reasoning graph**.  It integrates the following core components:

* **Reasoning Graph** (`ReasoningGraph` in `graph_manager.py`)
  * Directed multigraph where each node represents a concept, artefact or agent extracted from the archives and research.
  * Nodes have attributes such as `label`, `type`, `source`, `score` and `metadata`.
  * Edges represent relationships (influence, contradiction, derivation, extension) and carry `relation` and `weight` attributes.

* **Memetic Engine** (`MemeticEngine` in `memetic_algorithm.py`)
  * Applies a hybrid global/local search to the reasoning graph by mutating node scores and adding new relations.
  * Uses a `Critic` to evaluate each variant and retains improvements.
  * Inspired by memetic algorithms【230422289242979†L41-L87】 which combine evolutionary operators with local search for robust convergence.

* **Quarantine** (`Quarantine` in `quarantine.py`)
  * Identifies and isolates nodes with low confidence scores or high variance, preventing them from polluting reasoning until further validation.
  * Maintains a list of quarantined nodes and supports reintegration when scores improve.

* **Critic** (`Critic` in `critic.py`)
  * Computes a quality score for the entire graph based on edge density, mean node importance and structural balance.
  * Produces reports highlighting isolated nodes, hubs, dead ends, variance and recommendations for improvement.

* **Meta Agent** (`MetaAgent` in `meta_agent.py`)
  * Orchestrates the pipeline: loading data, running memetic evolution, applying quarantine, performing audits and saving the graph.
  * Configurable via `MetaConfig` for threshold values and iteration counts.

* **Integration Hooks** (`integration.py`)
  * Stubs for connecting to external data sources (APIs, web search, scientific repositories).  These can be extended to pull fresh facts into the graph.

* **Explainability Utilities** (`explainability.py`)
  * Functions to derive justification paths between concepts, summarise nodes and export the graph as a knowledge graph for explainable AI (XAI) applications【850674227268130†L45-L75】.


## Multi‑agent rationale

The architecture mirrors best practices from multi‑agent reasoning systems:

* **Modularity and specialisation**: Breaking down a monolithic agent into specialised modules (memetic engine, critic, quarantine) follows recommendations from LangGraph and other frameworks【906438729630143†L116-L139】.  Each component focuses on a single aspect of reasoning and can be evolved independently.
* **Distributed processing**: A graph‑centric approach enables decomposition of complex reasoning into node‑centric tasks.  GraphAgent‑Reasoner shows that such multi‑agent decomposition scales well and achieves high accuracy【166755538859472†L20-L37】.  Our memetic engine can be extended to spawn subagents per node or per community in the graph.
* **Knowledge graph integration**: Temporal and semantic relationships captured in knowledge graphs improve memory retention and explainability【928960283267357†L56-L114】.  This infrastructure supports exporting the reasoning graph to a knowledge‑graph format and linking to external ontologies.
* **Memetic evolution**: Combining evolutionary search with local refinement promotes robust exploration and exploitation of the reasoning space, as described in memetic algorithm literature【230422289242979†L41-L87】.


## Reasoning data flow

1. **Ingestion**: Data from archives, logs, research papers and external APIs are processed into a tabular form (CSV/JSON) with columns describing source/target concepts, relation types, scores and sources.
2. **Graph construction**: The `ReasoningGraph` ingests this data to create nodes and edges.  Additional metadata, such as memetic codes or disciplinary tags, can be added at this stage.
3. **Memetic evolution**: The `MemeticEngine` mutates the graph, exploring alternative weightings and connections, followed by local optimisation using the `Critic` for evaluation.
4. **Quarantine**: Nodes whose scores fall below a threshold are tagged as quarantined.  They remain in the graph but can be excluded from reasoning or flagged for review.
5. **Audit and feedback**: The `Critic` runs an audit to identify blind spots, hubs, dead ends and variance issues.  Recommendations are generated for graph improvement.
6. **Explainability and export**: Selected reasoning paths and concepts are summarised for human interpretation.  The graph can be exported to a knowledge‑graph format for integration with XAI pipelines.
7. **Iteration**: The pipeline can loop with new data or updated thresholds, enabling continuous evolution of the reasoning infrastructure.


## Extending the system

* **External Integrations**: Implement custom classes inheriting from `DataSource` in `integration.py` to connect to APIs like GitHub (via connectors), ArXiv, PubMed or custom endpoints.  Populate the `sources` registry so that the Meta Agent can fetch fresh knowledge.
* **Multi‑agent decomposition**: For large graphs, split the reasoning graph into communities or node sets.  Assign separate memetic engines or critics to each subgraph, then aggregate results.  This mirrors hierarchical agent architectures【906438729630143†L145-L160】.
* **Visualisation**: Use the scripts in `scripts` to render the graph with Graphviz or D3.js, or integrate with a React front‑end for interactive exploration.
* **CI/CD**: Configure GitHub Actions (see `.github/workflows`) to run tests, build docs and deploy the latest reasoning graph to GitHub Pages automatically.
