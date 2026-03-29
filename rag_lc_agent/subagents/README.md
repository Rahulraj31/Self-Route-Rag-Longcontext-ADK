# Subagents Module

This directory isolates the individual Google ADK Agents that make up the Self-Route pipeline. By decentralizing the agents into self-contained files, the system remains highly scalable and modular.

## 🤖 Available Agents

### 1. `rag.py` (RAG Datastore Agent)

- **Purpose**: Perform high-speed retrieval across the Vertex AI Datastore.
- **Mechanism**: Uses `VertexAiSearchTool` to find document chunks.
- **Strict Grounding**: Bound by intensive instructions to output exactly `not_answerable` if the exact factual details are absent from the retrieved chunks.

### 2. `evaluator.py` (The Output Judge)

- **Purpose**: Evaluate the downstream text from the RAG Agent.
- **Mechanism**: Utilizes Pydantic schemas (`EvalDecision`) to enforce strict JSON output formatting.
- **Reliable Pass-through**: Now includes the original `rag_answer` in its structured output to ensure the Router captures the exact word-for-word result without meta-commentary.
- **Failure Enforcement**: If the Candidate Answer contains phrases implying uncertainty or violates grounding rules, the Evaluator issues a `not_answerable` grade, triggering the LC fallback.

### 3. `long_context.py` (RC Fallback Agent)

- **Purpose**: The ultimate safety net.
- **Mechanism**: Receives the entire raw context from the specified local document folder. It performs deep reading comprehension to locate specific edge-case details missing from the basic RAG datastore chunks.
