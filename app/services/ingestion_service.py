from app.data.stock_api import get_stock_news
from app.rag.vector_db import VectorDB
import uuid

db = VectorDB()

def ingest_news(ticker):
    news = get_stock_news(ticker)

    texts = []
    metadatas = []
    ids = []

    for item in news:
        texts.append(item["text"])
        metadatas.append({
            "ticker": item["ticker"],
            "source": item["source"],
            "date": item["date"]
        })
        ids.append(str(uuid.uuid4()))

    db.add(texts, metadatas, ids)

    return {
        "ingested_items": len(texts),
        "ticker": ticker
    }