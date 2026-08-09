# AI Calling Agent

This project contains the FastAPI backend for the AI calling agent, plus the document ingestion and retrieval pipeline used for knowledge search and RAG-style responses.

## Environment configuration

Copy `.env.example` to `.env` and adjust the values for your environment.

Required or commonly used variables:

- `DATABASE_URL` — SQLAlchemy connection string
- `GEMINI_API_KEY` — Google Gemini key for LLM access
- `OPENROUTER_API_KEY` and `OPENROUTER_API_URL` — OpenRouter compatible LLM integration
- `EMBEDDING_PROVIDER` — `local` or `bge`
- `BGE_TOKENIZER_NAME` — tokenizer model for chunking when using the BGE setup
- `CHUNK_MAX_TOKENS` and `CHUNK_OVERLAP_TOKENS` — chunk sizing defaults
- `QDRANT_URL` — Qdrant server URL, for example `http://localhost:6333`
- `QDRANT_API_KEY` — optional API key for secured Qdrant deployments
- `QDRANT_COLLECTION` — default knowledge collection name
- `QDRANT_COLLECTIONS` — comma-separated list of collections

## Knowledge ingestion flow

The ingestion path is:

1. load a file from disk
2. split it into text chunks
3. generate embeddings
4. store vectors in Qdrant
5. record the document metadata in the local index

Supported document inputs include plain text, PDF, DOCX, PPTX, and HTML when the corresponding optional packages are installed.

## Local development

```bash
python -m venv .venv
. .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Tests

```bash
pytest -q
```

Set `QDRANT_URL` to run the live Qdrant smoke test.
