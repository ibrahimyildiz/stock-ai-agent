import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from app.data.knowledge import stock_knowledge

class ChromaStore:
    def __init__(self):
        self.client = chromadb.Client(
            Settings(
                persist_directory="./chroma_db",
                anonymized_telemetry=False
            )
        )

        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )

        self.collection = self.client.get_or_create_collection(
            name="stock_knowledge",
            embedding_function=self.embedding_function
        )

        self._load_data()

    def _load_data(self):
        if self.collection.count() == 0:
            self.collection.add(
                documents=stock_knowledge,
                ids=[str(i) for i in range(len(stock_knowledge))]
            )
            self.client.persist()  # IMPORTANT

    def search(self, query: str, k=3):
        results = self.collection.query(
            query_texts=[query],
            n_results=k
        )

        return results["documents"][0]