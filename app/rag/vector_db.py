import chromadb
from chromadb.config import Settings

class VectorDB:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path="/app/chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="stock_news"
        )

    def add(self, texts, metadatas, ids):
        self.collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )

    def search(self, query, k=5):
        return self.collection.query(
            query_texts=[query],
            n_results=k
        )