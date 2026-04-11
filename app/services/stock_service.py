# business logic (agent)

from app.rag.pipeline import rag_pipeline

def get_stock_recommendation(query: str):
    return rag_pipeline(query)