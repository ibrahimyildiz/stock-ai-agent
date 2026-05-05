from fastapi import APIRouter, Body
from pydantic import BaseModel

from app.core.container import Container
from app.agents.graph import build_graph
from app.data.stock_api import get_stock_news
from app.services.stock_service import get_stock_recommendation

router = APIRouter()

container = None
graph = None


def get_container():
    global container
    if container is None:
        container = Container()
    return container


def get_graph():
    global graph
    if graph is None:
        graph = build_graph()
    return graph


class ChatRequest(BaseModel):
    query: str


# =========================
# STOCK (legacy)
# =========================
@router.get("/recommend")
def recommend(q: str):
    return {"response": get_stock_recommendation(q)}


# =========================
# INGESTION
# =========================
@router.post("/ingest")
def ingest(payload: dict = Body(...)):

    container = get_container()

    ticker = payload.get("ticker")
    if not ticker:
        return {"error": "ticker required"}

    articles = get_stock_news(ticker)

    result = container.ingestion_service.ingest_news(ticker, articles)

    container.build_bm25()

    return {
        "status": "success",
        "ticker": ticker,
        "count": result["ingested_items"]
    }


# =========================
# CHAT (MAIN)
# =========================
@router.post("/chat")
async def chat_endpoint(request: ChatRequest):

    graph = get_graph()

    result = await graph.ainvoke({
        "query": request.query
    })

    return result.get("final_output", result)


# =========================
# ANALYZE (alias)
# =========================
@router.get("/analyze")
async def analyze_stock(query: str):

    graph = get_graph()

    result = await graph.ainvoke({
        "query": query
    })

    return result.get("final_output", result)


# =========================
# DEBUG: VECTOR DB STATUS
# =========================
@router.get("/debug/db")
def debug_db():

    try:
        container = get_container()
        collection = container.vector_store.collection

        data = collection.peek(5)

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

    except Exception as e:
        return {"error": str(e)}


# =========================
# DEBUG: FULL COLLECTION
# =========================
@router.get("/debug/full")
def debug_full():

    try:
        container = get_container()
        collection = container.vector_store.collection

        data = collection.get()

        return {
            "ids": data.get("ids", []),
            "documents": data.get("documents", []),
            "metadatas": data.get("metadatas", [])
        }

    except Exception as e:
        return {"error": str(e)}


# =========================
# DEBUG: RETRIEVAL TEST
# =========================
@router.get("/debug/retrieval")
def debug_retrieval(query: str):

    try:
        container = get_container()

        ticker = None
        results = container.retriever.retrieve(query)

        output = []

        for i, doc in enumerate(results):
            output.append({
                "index": i,
                "text": getattr(doc, "page_content", str(doc)),
                "metadata": getattr(doc, "metadata", {})
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