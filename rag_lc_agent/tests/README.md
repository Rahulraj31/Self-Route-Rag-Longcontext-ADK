# Automated Evaluation Suite

This directory contains the testing framework that algorithmically validates the Self-Route architecture's intelligence, routing accuracy, and hallucination resistance.

## 🧪 Components

### 1. `test_data.py`

Houses the hardcoded test dictionary representing three strict evaluation topologies:

- **Unique Context**: Data existing purely in the RAG datastore.
- **High RAG Context**: The RAG context greatly exceeds the local TXT file summaries.
- **High LC Context**: The local TXT files greatly exceed the basic RAG summaries.

Each test case contains the original query paired with the absolute expected Ground Truth.

### 2. `eval_metrics.py`

Defines the **LLM-as-a-Judge** instance. Rather than relying on rigid semantic exact-matches, this agent comprehends the core intent of the pipeline's answers and grades them strictly (1-5 scale) on:

- **Correctness**: Adherence to the established Ground Truth.
- **Faithfulness**: Detection of hallucinations or speculative statements.
- **Completeness**: Verification that multi-part clauses within the user query were fully addressed.

### 3. `run_evals.py`

The master execution script. It loops over the **12 baseline queries**, invokes the core RAG router asynchronously, extracts the resulting text, and pipes it directly into the Judge LLM. The resulting evaluation matrix is exported securely as a `.csv` file.
