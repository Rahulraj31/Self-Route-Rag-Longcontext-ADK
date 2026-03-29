# Self-Route LLM Agent Architecture

> **Research Implementation**: This project is a practical implementation of **Self-Route**, a method introduced in the paper **["Retrieval Augmented Generation or Long-Context LLMs? A Comprehensive Study and Hybrid Approach"](https://arxiv.org/abs/2407.16833)** (arXiv:2407.16833). Self-Route reduces computation cost by dynamically routing queries to RAG or Long-Context LLMs based on model self-reflection.

## 🏗️ Core Architecture
The system consists of three primary agents orchestrated by a top-level Conversational Router:

1. **RAG Extraction Agent** — Rapidly searches the Vertex AI Datastore. Instructed to strictly output `not_answerable` if the retrieved context is insufficient.
2. **Evaluator Judge Agent** — Critiques the RAG output with structured Pydantic output. Issues a `not_answerable` decision if the answer is ungrounded or incomplete, signalling the router to fallback.
3. **Long Context (LC/RC) Agent** — The ultimate fallback. Ingests raw text files directly from disk for deep reading comprehension, designed to answer what the basic datastore chunks missed.

## 📂 Repository Structure
```
Self-Route LLM/
│
├── README.md                    # This file
├── generate_rag_files.py        # Utility to procedurally generate .pdf / .docx test data
│
└── rag_lc_agent/
    ├── agent.py                 # ADK Web entrypoint, Root Conversational Router
    ├── config.py                # Centralized .env variable management
    ├── instructions.py          # All LLM system prompts (routing, RAG, eval, LC)
    ├── tool.py                  # load_docs() utility for Long Context ingestion
    ├── .env                     # Environment configuration (do not commit)
    │
    ├── subagents/               # Individual agent definitions
    │   ├── rag.py               # Vertex AI Search Agent
    │   ├── evaluator.py         # Output evaluation with structured JSON output
    │   ├── long_context.py      # Deep reading comprehension fallback Agent
    │   └── README.md            # Subagents module documentation
    │
    ├── tests/
    │   ├── test_data.py         # 9 Categorized test queries with Ground Truth answers
    │   ├── eval_metrics.py      # LLM-as-a-Judge scoring definitions
    │   ├── run_evals.py         # Main automated evaluation script → outputs CSV
    │   └── README.md            # Tests module documentation
    │
    └── docs/                    # Ground-truth text files for the Long Context Agent
        ├── remote_work_policy.txt
        ├── leave_policy.txt
        └── code_of_conduct.txt
```

## ⚙️ Setup Instructions

### 1. Prerequisites
Ensure you have Python 3.10+ and access to a Google Cloud Project with Vertex AI and Vertex AI Search APIs enabled.

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment variables
Populate `rag_lc_agent/.env` with your values:
```bash
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
DATASTORE_RESOURCE=projects/<PROJECT_ID>/locations/global/collections/default_collection/dataStores/<DATASTORE_ID>
DOCS_FOLDER=./docs
MAX_RESULTS=3
AGENT_MODEL=gemini-2.5-flash
```

### 4. (Optional) Generate test datasets for Vertex Datastore
Run the generation script to create `.pdf` and `.docx` files for upload to your datastore:
```bash
pip install fpdf python-docx
python generate_rag_files.py
```

## 🚀 Running the Agent

### Start ADK Web Interface
```bash
adk web
```
Open your browser at `http://localhost:8000` to interact with the Self-Route conversational agent.

### Run Automated Evaluation Suite
```bash
python rag_lc_agent/tests/run_evals.py
```
This will run 9 categorized queries (RAG Unique, RAG > LC, LC > RAG) and export the evaluation results to `rag_lc_agent/tests/evaluation_results.csv`.
