# repochat - codebase intelligence system

a rag based tool that lets you ask natural-language questions about a software repository and get answers grounded in the actual code, with file and line citations.

built to run on a laptop with **8GB RAM and no GPU**, using **Gemini API** for LLM inference and local embeddings for retrieval.

---

## Features

* repository indexing
* structure-aware code chunking
* local code embeddings with `all-MiniLM-L6-v2`
* persistent vector storage with ChromaDB
* semantic code search
* gemini-powered answers
* file and line-level citations
* supports python, javascript, typescript, java, go, c/c++ and rust

---

## Architecture

```text
repository
     │
     ▼
file scanner
     │
     ▼
code chunker
     │
     ▼
local embeddings
     │
     ▼
chromaDB
     │
     ▼
vector search
     │
     ▼
gemini
     │
     ▼
answer + citations
```

---

## tech stack

| component       | technology            |
| --------------- | --------------------- |
| Backend         | FastAPI               |
| Frontend        | Streamlit             |
| LLM             | Gemini API            |
| Embeddings      | Sentence Transformers |
| Vector Database | ChromaDB              |
| Language        | Python                |

---

## Project Structure

```text
codebase-intelligence/
├── backend/
│   ├── api/
│   ├── ingestion/
│   ├── chunking/
│   ├── embeddings/
│   ├── vectorstore/
│   ├── llm/
│   ├── rag/
│   ├── config.py
│   └── main.py
├── frontend/
│   └── app.py
├── data/
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── run.py
```

---

## Setup

### 1. clone the repository

```bash
git clone <your-repo-url>
cd codebase-intelligence
```

### 2. create a virtual environment

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. install dependencies

```bash
pip install -r requirements.txt
```

### 4. configure gemini

Create an API key from [Google AI Studio](https://aistudio.google.com/apikey).

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## run

start the backend:

```bash
python run.py
```

start the frontend in another terminal:

```bash
streamlit run frontend/app.py
```

open the streamlit interface and enter the path of the repository you want to analyze.

---


## Current Scope — Phase 1

Phase 1 focuses on the core RAG pipeline:

* vector-based retrieval
* heuristic structural chunking
* local embeddings
* chromaDB storage
* gemini-based generation
* code citations

### Limitations

* No hybrid BM25 + vector retrieval
* No dependency graph
* No impact analysis
* No incremental indexing
* No Git awareness

---

## Roadmap

### Phase 2

* tree-sitter based code parsing
* hybrid BM25 + vector retrieval
* improved citations
* better code metadata

### Phase 3

* dependency graph
* function and class relationships
* impact analysis

### Phase 4

* incremental indexing
* file hashing
* git-aware retrieval

### Phase 5

* automated evaluation
* recall@5
* citation accuracy
* latency benchmarking

