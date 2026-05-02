# search logic

from app.rag.vector_db import query_documents
from app.utils.ticker_utils import extract_ticker

def retrieve_context(query: str):
    ticker = extract_ticker(query)
    results = query_documents(query, ticker=ticker)

    documents = results.get("documents") or [[]]
    docs = documents[0] if documents else []

    return docs