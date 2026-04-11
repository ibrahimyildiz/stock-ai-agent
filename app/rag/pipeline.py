# RAG pipeline (important - This is your RAG brain)

from app.rag.retriever import retrieve_context
from app.core.llm import call_llm

def rag_pipeline(query: str):
    context = retrieve_context(query)

    prompt = f"""
    You are an expert stock analyst.

    Use ONLY the context below to answer.

    Context:
    {context}

    Question:
    {query}

    Give:
    - Recommendation (Buy / Sell / Hold)
    - Reason (based on context)
    - Confidence level (Low/Medium/High)
    """

    return call_llm(prompt)