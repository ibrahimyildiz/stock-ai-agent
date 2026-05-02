from app.data.stock_api import get_stock_news
from app.rag.vector_db import add_documents
import uuid

def ingest_news(ticker: str):
    articles = get_stock_news(ticker)

    texts = []
    metadatas = []
    ids = []

    for i, article in enumerate(articles):
        texts.append(article["text"])

        safe_date = article["date"].replace(":", "-")

        metadatas.append({
            "ticker": article["ticker"],
            "source": article.get("source", "unknown"),
            "date": article.get("date", ""),
            "external_id": f"{ticker}_{safe_date}_{i}"
        })

        ids.append(str(uuid.uuid4()))

    add_documents(texts, metadatas, ids)

    return {
        "ingested_items": len(texts),
        "ticker": ticker
    }