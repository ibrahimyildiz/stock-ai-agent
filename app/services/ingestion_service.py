from langchain_core.documents import Document
import uuid


class IngestionService:

    def __init__(self, vector_store):
        self.vector_store = vector_store

    def ingest_news(self, ticker: str, articles):

        documents = []
        ids = []
        metadatas = []

        for i, article in enumerate(articles):

            doc = Document(
                page_content=article.get("text", ""),
                metadata={
                    "ticker": article.get("ticker", ticker),
                    "source": article.get("source", "unknown"),
                    "date": article.get("date", ""),
                    "external_id": f"{ticker}_{i}"
                }
            )

            documents.append(doc)
            ids.append(str(uuid.uuid4()))
            metadatas.append(doc.metadata)

        self.vector_store.add_documents(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )

        return {
            "ingested_items": len(documents),
            "ticker": ticker
        }