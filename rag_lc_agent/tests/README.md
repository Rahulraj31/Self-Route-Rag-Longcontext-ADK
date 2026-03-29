# Automated Evaluation Suite

This directory contains the testing framework that validates the **Self-Route** architecture's intelligence, routing accuracy, and hallucination resistance.

## 🧪 Test Case Design Philosophy

Our evaluation suite intentionally includes RAG-answerable, long-context, ambiguous, retrieval-failure, and multi-hop queries to verify correct routing, fallback behavior, and cross-document reasoning in the Self-Route architecture.

## 🛠️ Components

### 1. `test_data.py`

Houses the benchmark test cases categorized into 6 specialized topologies:

- **RAG_ONLY**: Single fact answerable via standard retrieval.
- **LONG_CONTEXT_ONLY**: High-precision answer exists only in the full local document.
- **AMBIGUOUS**: Query missing constraints requiring a full policy scan to avoid guessing.
- **FAIL_RETRIEVAL**: Cases where the retriever likely returns an incorrect or partial chunk.
- **EDGE_CASE_SHORT**: Very short/unclear query (e.g., "NYC Hotel?") that requires deep context.
- **EDGE_CASE_MULTI_HOP**: Requires combining multiple sections or documents for a complete answer.

### 2. `eval_metrics.py`

Defines the **LLM-as-a-Judge** logic. It grades the pipeline's answers on a 1-5 scale across:

- **Correctness**: Adherence to the established Ground Truth.
- **Faithfulness**: Detection of hallucinations or speculative statements.
- **Completeness**: Verification that all parts of the query were addressed.

### 3. `run_evals.py`

The master execution script. It follows the **4-agent routing flow**:

1.  **Retriever** fetches chunks.
2.  **Evaluator** decides `answerable` or `not_answerable`.
3.  **RAG** or **Long Context** generates the final response.

## 📊 Evaluation Output (`evaluation_results.csv`)

The script generates a CSV with the following columns:

| Column              | Description                                             |
| :------------------ | :------------------------------------------------------ |
| **Category**        | The test category (RAG_ONLY, AMBIGUOUS, etc.)           |
| **Query**           | The user input                                          |
| **Ground Truth**    | The reference answer from the source documents          |
| **Expected Route**  | The ground-truth routing path (`rag` or `long_context`) |
| **Actual Route**    | The actual path taken by the agent                      |
| **Route Correct**   | Boolean (True/False) comparison                         |
| **Final Answer**    | The actual text response returned                       |
| **Correctness**     | Judge score (1-5)                                       |
| **Faithfulness**    | Judge score (1-5)                                       |
| **Completeness**    | Judge score (1-5)                                       |
| **Judge Reasoning** | The LLM's explanation for the scores                    |

## 🚀 How to Run

```bash
python -m rag_lc_agent.tests.run_evals
```
