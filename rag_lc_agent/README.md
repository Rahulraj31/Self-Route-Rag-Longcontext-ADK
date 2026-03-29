# `rag_lc_agent` Module

This directory contains the core logic for the **Self-Route** RAG system. It is structured as a modular Google ADK application that dynamically chooses between a Vertex AI Search pipeline and a local Long-Context fallback.

## 📂 Folder Structure

### 1. `subagents/`

Contains the individual ADK Agents that form the Self-Route pipeline:

- **`retreiver.py`**: [NEW] Fetches document chunks from Vertex AI Search using the `VertexAiSearchTool`.
- **`evaluator.py`**: Grades the `retrieved_chunks` for answerability (gatekeeper logic).
- **`rag.py`**: Generates the final answer using only the provided chunks (grounded generation).
- **`long_context.py`**: Fallback agent that reads entire documents from the `docs/` folder for synthesis.

### 2. `docs/`

The ground-truth repository for the Long-Context agent. Contains detailed `.txt` policies (e.g., `travel_policy.txt`, `parental_leave_appendix.txt`) that provide high-resolution data often missing from RAG chunks.

### 3. `tests/`

The automated evaluation framework. Includes `test_data.py` (12 baseline benchmark cases) and `run_evals.py` (main execution script for tracking routing accuracy).

---

## 🛠️ Core Files

- **`agent.py`**: The entrypoint for the Self-Route Router. It acts as an orchestrater, calling the 4 sub-agents as tools to decide the most efficient path.
- **`config.py`**: Centralized configuration and environment variable loader.
- **`instructions.py`**: The "brain" of the system. Contains all the specialized System Prompts and grounding rules for each agent.
- **`tool.py`**: A helper utility used by the Long-Context agent to ingest all local documents into a single flattened context string.
- **`__init__.py`**: Standard Python package marker.
- **`.env`**: Local environment variables (API keys, project IDs, datastore paths).

---

## ⚙️ Configuration

The module is primarily configured via `config.py`, which reads from the `.env` file. Key parameters include:

- **`DATASTORE_RESOURCE`**: The full URI to your Vertex AI Search datastore.
- **`AGENT_MODEL`**: The LLM backing all agents (default: `gemini-2.5-flash`).
- **`DOCS_FOLDER`**: Path to the local policy repository.
- **`MAX_RESULTS`**: Number of chunks the retriever should fetch per query.
