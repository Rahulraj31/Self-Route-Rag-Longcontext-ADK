# `rag_lc_agent` Module

This directory contains the core logic for the Self-Route RAG system. It is structured as a modular Google ADK application that dynamically chooses between a Vertex AI Search pipeline and a local Long-Context fallback.

## 📂 Folder Structure

### 1. `subagents/`

Contains the individual ADK Agents:

- `rag.py`: Performs initial retrieval using the `VertexAiSearchTool`.
- `evaluator.py`: Grades the RAG response for answerability and grounding (Pydantic-based).
- `long_context.py`: Fallback agent that reads entire documents from the `docs/` folder.

### 2. `docs/`

The ground-truth repository for the Long-Context agent. Contains detailed `.txt` policies like `travel_policy.txt` and `parental_leave_appendix.txt` which provide high-resolution data intentionally missing from the RAG chunks.

### 3. `tests/`

The automated evaluation framework. Includes `test_data.py` (12 baseline benchmark cases) and `run_evals.py` (main execution script).

---

## 🛠️ Core Files

- **`agent.py`**: The entrypoint for the Self-Route Router. It manages the conversational history and delegates work to either the `rag_pipeline` or the `long_context_agent`.
- **`config.py`**: Centralized configuration and environment variable loader.
- **`instructions.py`**: The "brain" of the system. Contains all the specialized System Prompts and grounding rules for each agent.
- **`tool.py`**: A helper utility used by the Long-Context agent to ingest all local documents into a single flattened context string.
- **`__init__.py`**: Standard Python package marker.
- **`.env`**: Local environment variables (API keys, project IDs, datastore paths).

---

## ⚙️ Configuration

The module is primarily configured via `config.py`, which reads from the `.env` file. Key parameters include:

- `DATASTORE_RESOURCE`: The full URI to your Vertex AI Search datastore.
- `AGENT_MODEL`: The LLM backing all agents (default: `gemini-2.5-flash`).
- `DOCS_FOLDER`: Path to the local policy repository.
