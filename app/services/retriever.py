from app.services.ranker import rank_documents
from app.services.bm25_retriever import BM25Retriever


def retrieve_documents(vector_store, all_documents, query, k=5):

    # Vector search
    vector_docs = vector_store.similarity_search(query, k=10)

    # BM25 search
    bm25 = BM25Retriever(all_documents)

    bm25_docs = bm25.search(query, k=10)

    # Merge results
    combined_docs = vector_docs + bm25_docs

    # Remove duplicates
    unique_docs = []

    seen = set()

    for doc in combined_docs:
        content = doc.page_content

        if content not in seen:
            seen.add(content)
            unique_docs.append(doc)

    # Rank
    ranked_docs = rank_documents(unique_docs, query)

    return ranked_docs[:k]