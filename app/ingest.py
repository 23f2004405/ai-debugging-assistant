from pathlib import Path
import chromadb
from langchain_ollama import OllamaEmbeddings
from app.config import OLLAMA_BASE_URL, EMBED_MODEL, COLLECTION_NAME

DOC_DIR = Path("data/docs")
DB_DIR = Path("chroma_db")

def main():
    client = chromadb.PersistentClient(path=str(DB_DIR))
    collection = client.get_or_create_collection(COLLECTION_NAME)
    embeddings = OllamaEmbeddings(model=EMBED_MODEL, base_url=OLLAMA_BASE_URL)

    docs, ids = [], []
    for path in DOC_DIR.glob("*.md"):
        docs.append(path.read_text(encoding="utf-8"))
        ids.append(path.name)

    vectors = embeddings.embed_documents(docs)
    collection.upsert(ids=ids, documents=docs, embeddings=vectors)
    print(f"Indexed {len(docs)} documents.")

if __name__ == "__main__":
    main()
