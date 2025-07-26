# Cross‑reference log

This log maps the contents of the reasoning archives, logs and reports to the modules and design decisions in this repository.  It is intended to provide traceability between the input artefacts and the final reasoning infrastructure.

## Archive files

| Archive / file | Summary of contents | Used in |
|---|---|---|
| **evolution_god_analysis.md** | Explores the memetic evolution of the concept of God: from a primitive explanation stopper to a mathematical abstraction and AI “black box”.  Highlights the cyclical nature of myths and reasoning, and the need for meta‑analysis【301593799283921†screenshot】. | Informed the `memetic_algorithm` design — we incorporated phases of mutation and abstraction reminiscent of the conceptual transitions described.  Also inspired the quarantine mechanism for parasitic memetic branches. |
| **koach_roma_analysis.md** (analysis of “Коуч и Рома”) | Deconstructs a user–bot confrontation where the system fails to interpret video context and over‑guards its responses.  Emphasises the need for meta‑doubt, self‑testing and critic modules【301593799283921†screenshot】. | Motivated the `critic` module and its audit functions for detecting blind spots, simulations and over‑guarding.  Also underscored the importance of a trace‑based “Coach/EXCAVATOR” mode, reflected in the `MetaAgent` pipeline. |
| **ULTIMAI_v4.4.1_FullDeploy** scripts | Provides various JavaScript modules (`reasoning_modulator.js`, `meta_synthesizer.js`, etc.) and Python prototypes (`hyperreasoning_2_core.py`, `ultimai_reasoning_graph.py`) for graph manipulation, quarantine logic and patch management. | Served as a blueprint for the `ReasoningGraph` implementation and memetic engine.  The prototypes helped define the quarantine threshold and local search heuristics. |
| **CSV file (___________________________________________________.csv)** | Contains pairs of source/target concepts with relations and scores. | Used as a template for the expected input format for `ReasoningGraph.from_csv()`.  Column names and semantics (source_id, target_id, relation, scores, files) were mirrored in the parser. |
| **MEMES and Эволюция bога text files** | Collections of memetic experiments, memes and philosophical notes. | Contributed to the overall philosophy of using memetic algorithms for reasoning and emphasised the role of absurdity and paradox in idea generation. |
| **Report PDFs (“Анализ и интеграция данных”)** | Describe integration of multiple data sources and analysis pipelines. | Inspired the modular design of ingestion and integration hooks (`integration.py`) and the need for cross‑validation and self‑testing. |
| **Conversation logs (`Агентное исследование.txt`, `НАГИТХАБ!.txt`)** | Capture earlier interactions with ChatGPT about agent modes, GitHub integration and reasoning modes. | Provided context for enabling GitHub access (though connectors only allow reads) and emphasised user requirements for memetic flexibility, critic modules and external API integration. |

## External research references

| External source | Key points | Influence |
|---|---|---|
| **LangGraph / multi‑agent frameworks**【906438729630143†L116-L139】【906438729630143†L145-L160】 | Advocates decomposing large tasks into specialised agents for improved modularity and control; describes different agent architectures (network, supervisor, hierarchical). | Guided the modular design of the `MetaAgent`, `Critic`, `Quarantine` and `MemeticEngine`.  Motivated the possibility of hierarchical decomposition if the graph scales. |
| **GraphAgent‑Reasoner**【166755538859472†L20-L37】 | Demonstrates that decomposing graph reasoning into node‑centric tasks and distributing them across agents improves scalability and accuracy. | Justified the use of a graph‑centric representation and laid the groundwork for future extensions into node‑level agents. |
| **KG4XAI / KG4Diagnosis / Knowledge graph XAI**【928960283267357†L56-L114】【850674227268130†L45-L75】 | Highlights the benefits of knowledge graphs for storing temporal relations and improving explainability; outlines roles of knowledge graphs in feature extraction, relation extraction, integration, constraints enforcement and natural language explanations. | Led to the inclusion of `explainability.py` and the ability to export the reasoning graph as a knowledge graph for XAI purposes.  Encouraged the separation of reasoning and explanation layers. |
| **Memetic algorithms**【230422289242979†L41-L87】 | Describe how evolutionary operators combined with local search yield robust and flexible optimisation strategies. | Inspired the design of `MemeticEngine` with mutation and local search phases, and the hybrid global/local approach. |

## Reasoning logs and reports

* **`report_full_final.md` and related summaries**: Provided a synthesis of previous analyses, identified missing imports and mismatches in the existing code, and highlighted recommendations for quarantine, meta‑synthesizer and reasoning‑modulator modules.  These insights were incorporated into the final design.

* **Earlier chat discussions**: Guided our understanding of the user’s goals (multi‑agent flexibility, memetic evolution, critic/self‑test, hypergraph visualisation, GitHub integration) and shaped the functional requirements for this infrastructure.