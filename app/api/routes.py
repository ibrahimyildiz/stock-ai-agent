# API endpoints

from fastapi import APIRouter
from fastapi import Body
from app.services.stock_service import get_stock_recommendation
from app.services.ingestion_service import ingest_news

router = APIRouter()

@router.get("/recommend")
def recommend(q: str):
    result = get_stock_recommendation(q)
    return {"response": result}

@router.post("/ingest")
def ingest(payload: dict = Body(...)):
    ticker = payload.get("ticker")

    result = ingest_news(ticker)

    return {
        "status": "success",
        "ticker": ticker,
        "count": result["ingested_items"]
    }