# AI Support Engineer

A compact portfolio project demonstrating an agentic AI support workflow.

## Features
- FastAPI backend
- LangGraph multi-step workflow
- RAG over technical documentation with Chroma + Ollama embeddings
- Local codebase search tool
- Structured support response
- Simple browser UI
- Fully local LLM development with Ollama

## Run

Install Python 3.11+, Ollama, then:

```bash
ollama pull qwen2.5:3b
ollama pull nomic-embed-text

python -m venv .venv
# Windows:
.venv\Scripts\activate

pip install -r requirements.txt
python -m app.ingest
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000

## Demo

Try:
> My POST /users endpoint returns a 500 error when I create an account with an email that already exists. What is wrong and how should I fix it?

The agent retrieves documentation and searches the sample codebase before diagnosing the problem.

## Resume bullet

Built an agentic AI support engineer using FastAPI and LangGraph, combining local RAG over technical documentation with a code-search tool and structured LLM outputs to diagnose software issues and recommend fixes.
