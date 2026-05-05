from collections import defaultdict

class RRF:
    def __init__(self, k: int = 60):
        self.k = k

    def fuse(self, vector_docs, bm25_docs):
        scores = defaultdict(float)
        doc_map = {}

        def add(docs, weight=1.0):
            for rank, doc in enumerate(docs):
                key = doc.page_content
                scores[key] += weight / (self.k + rank + 1)
                doc_map[key] = doc

        add(vector_docs, weight=1.0)
        add(bm25_docs, weight=1.0)

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        return [doc_map[k] for k, _ in ranked]