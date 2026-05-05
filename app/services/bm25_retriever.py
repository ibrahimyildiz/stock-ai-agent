from rank_bm25 import BM25Okapi
from langchain_core.documents import Document


class BM25Retriever:

    def __init__(self, documents):
        # Always normalize first
        self.documents = [
            doc for doc in documents
            if hasattr(doc, "page_content") and doc.page_content
        ]

        if len(self.documents) == 0:
            self.bm25 = None
            self.tokenized_docs = []
            return

        self.tokenized_docs = [
            doc.page_content.lower().split()
            for doc in self.documents
        ]

        self.bm25 = BM25Okapi(self.tokenized_docs)

    def search(self, query, k=5):

        if not self.bm25:
            return []

        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)

        scored_docs = list(zip(self.documents, scores))
        scored_docs.sort(key=lambda x: x[1], reverse=True)

        return [doc for doc, _ in scored_docs[:k]]