import os
import chromadb

CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = os.getenv("CHROMA_PORT", "8000")

client = chromadb.HttpClient(
    host=CHROMA_HOST,
    port=int(CHROMA_PORT)
)

collection = client.get_or_create_collection("stocks")


def search_vectors(query_embedding, k=5):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    return results