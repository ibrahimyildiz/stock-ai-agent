import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from app.data.knowledge import stock_data
from app.rag.chunker import chunk_text

class SimpleVectorStore:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.texts = []
        self.metadata = []
        self.vectors = []

        self._load_data()

    def _load_data(self):
        for item in stock_data:
            chunks = chunk_text(item["text"])

            for chunk in chunks:
                self.texts.append(chunk)
                self.metadata.append({
                    "ticker": item["ticker"],
                    "source": item["source"],
                    "date": item["date"]
                })

        self.vectors = self.model.encode(self.texts)

    def search(self, query: str, k=3, ticker=None):
        query_vec = self.model.encode([query])
        similarities = cosine_similarity(query_vec, self.vectors)[0]

        # Filter by ticker if provided
        if ticker:
            filtered_indices = [
                i for i, meta in enumerate(self.metadata)
                if meta["ticker"] == ticker
            ]
        else:
            filtered_indices = list(range(len(self.texts)))

        scored = [(i, similarities[i]) for i in filtered_indices]
        scored.sort(key=lambda x: x[1], reverse=True)

        top_k = scored[:k]

        return [self.texts[i] for i, _ in top_k]

    def add_documents(self, new_data):
        new_texts = []
        new_metadata = []

        for item in new_data:
            chunks = chunk_text(item["text"])

            for chunk in chunks:
                new_texts.append(chunk)
                new_metadata.append({
                    "ticker": item["ticker"],
                    "source": item["source"],
                    "date": item["date"]
                })

        new_vectors = self.model.encode(new_texts)

        if len(self.texts) == 0:
            self.texts = new_texts
            self.metadata = new_metadata
            self.vectors = new_vectors
        else:
            self.texts.extend(new_texts)
            self.metadata.extend(new_metadata)
            self.vectors = np.vstack([self.vectors, new_vectors])