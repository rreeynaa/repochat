# Codebase Intelligence System

A RAG-based tool that lets you ask natural-language questions about a software repository and get answers grounded in the actual code, with file and line citations.

Built to run on a laptop with **8GB RAM and no GPU**, using **Gemini API** for LLM inference and local embeddings for retrieval.

---

## Features

* Repository indexing
* Structure-aware code chunking
* Local code embeddings with `all-MiniLM-L6-v2`
* Persistent vector storage with ChromaDB
* Semantic code search
* Gemini-powered answers
* File and line-level citations
* Supports Python, JavaScript, TypeScript, Java, Go, C/C++, and Rust

---

## Architecture

```text
Repository
     │
     ▼
File Scanner
     │
     ▼
Code Chunker
     │
     ▼
Local Embeddings
     │
     ▼
ChromaDB
     │
     ▼
Vector Search
     │
     ▼
Gemini
     │
     ▼
Answer + Citations
```

---

## Tech Stack

| Component       | Technology            |
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

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd codebase-intelligence
```

### 2. Create a virtual environment

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS**

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Gemini

Create an API key from [Google AI Studio](https://aistudio.google.com/apikey).

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## Run

Start the backend:

```bash
python run.py
```

Start the frontend in another terminal:

```bash
streamlit run frontend/app.py
```

Open the Streamlit interface and enter the path of the repository you want to analyze.

---

## Example

**Question**

```text
Where is authentication implemented?
```

**Response**

```text
Authentication is implemented in the auth module,
where user credentials are validated and tokens are generated.

Citations:
src/auth.py:12-38
```

---

## Current Scope — Phase 1

Phase 1 focuses on the core RAG pipeline:

* Vector-based retrieval
* Heuristic structural chunking
* Local embeddings
* ChromaDB storage
* Gemini-based generation
* Code citations

### Limitations

* No hybrid BM25 + vector retrieval
* No dependency graph
* No impact analysis
* No incremental indexing
* No Git awareness

---

## Roadmap

### Phase 2

* Tree-sitter based code parsing
* Hybrid BM25 + vector retrieval
* Improved citations
* Better code metadata

### Phase 3

* Dependency graph
* Function and class relationships
* Impact analysis

### Phase 4

* Incremental indexing
* File hashing
* Git-aware retrieval

### Phase 5

* Automated evaluation
* Recall@5
* Citation accuracy
* Faithfulness
* Latency benchmarking

---

## License

MIT License
