from pathlib import Path
import chromadb
from langchain_ollama import OllamaEmbeddings
from app.config import OLLAMA_BASE_URL, EMBED_MODEL, COLLECTION_NAME

DB_DIR = Path("chroma_db")

def get_collection():
    client = chromadb.PersistentClient(path=str(DB_DIR))
    return client.get_or_create_collection(COLLECTION_NAME)

def search_docs(query: str, k: int = 4) -> list[str]:
    collection = get_collection()
    if collection.count() == 0:
        return []
    embeddings = OllamaEmbeddings(model=EMBED_MODEL, base_url=OLLAMA_BASE_URL)
    vector = embeddings.embed_query(query)
    result = collection.query(query_embeddings=[vector], n_results=k)
    return result.get("documents", [[]])[0]
