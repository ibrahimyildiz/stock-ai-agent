class Retriever:

    def __init__(self, vector_store, bm25=None):
        self.vector_store = vector_store
        self.bm25 = bm25

    def retrieve(self, query: str, top_k: int = 20):

        vector_docs = self.vector_store.similarity_search(query, k=top_k)

        bm25_docs = []
        if self.bm25:
            bm25_docs = self.bm25.get_relevant_documents(query)[:top_k]

        return self._merge(vector_docs, bm25_docs)

    def _merge(self, vector_docs, bm25_docs):
        # simple MVP merge (you later upgrade to RRF)
        return list({id(d): d for d in (vector_docs + bm25_docs)}.values())