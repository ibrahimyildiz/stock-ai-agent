# API endpoints

from fastapi import APIRouter
from fastapi import Body
from app.services.stock_service import get_stock_recommendation
from app.services.ingestion_service import ingest_news

router = APIRouter()

# --------------------
# STOCK
# --------------------
@router.get("/recommend")
def recommend(q: str):
    result = get_stock_recommendation(q)
    return {"response": result}

# --------------------
# INGESTION
# --------------------
@router.post("/ingest")
def ingest(payload: dict = Body(...)):
    ticker = payload.get("ticker")

    result = ingest_news(ticker)

    return {
        "status": "success",
        "ticker": ticker,
        "count": result["ingested_items"]
    }

# --------------------
# DEBUG
# --------------------
@router.get("/debug/db")
def debug_db():
    from app.rag.vector_db import collection

    """
    data = collection.get() # fetches all
    data = collection.query(
                query_texts=["apple earnings"],
                n_results=5
            )
    """
    data = collection.peek(3) # fetches only 3

    results = []

    for i in range(len(data.get("ids", []))):
        results.append({
            "id": data["ids"][i],
            "document": data["documents"][i],
            "metadata": data["metadatas"][i]
        })

    return {
        "count": collection.count(),
        "results": results
    }

@router.get("/debug/full")
def debug_full():
    from app.rag.vector_db import collection

    data = collection.get()

    return {
        "ids": data.get("ids"),
        "documents": data.get("documents"),
        "metadatas": data.get("metadatas")
    }

@router.get("/debug/retrieval")
def debug_retrieval(query: str):
    try:
        from app.rag.vector_db import query_documents
        from app.utils.ticker_utils import extract_ticker

        ticker = extract_ticker(query)
        results = query_documents(query, ticker=ticker)

        documents = results.get("documents") or [[]]
        metadatas = results.get("metadatas") or [[]]
        ids = results.get("ids") or [[]]

        docs = documents[0] if documents else []
        metas = metadatas[0] if metadatas else []
        id_list = ids[0] if ids else []

        output = []

        for i in range(len(docs)):
            output.append({
                "id": id_list[i] if i < len(id_list) else None,
                "text": docs[i],
                "metadata": metas[i] if i < len(metas) else {}
            })

        return {
            "query": query,
            "count": len(output),
            "results": output
        }

    except Exception as e:
        import traceback
        return {
            "error": str(e),
            "trace": traceback.format_exc()
        }

# --------------------
# CHAT
# --------------------
@router.post("/chat")
def chat_endpoint(query: str):
    from app.services.ollama_client import generate_response
    return {"response": generate_response(query)}