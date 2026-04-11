# search logic

from app.rag.vector_db import VectorDB

db = VectorDB()

def retrieve_context(query: str):
    results = db.search(query)

    docs = results.get("documents", [[]])[0]

    return docs