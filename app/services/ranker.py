from datetime import datetime
import math
from langchain_core.documents import Document


IMPORTANT_KEYWORDS = {
    "earnings": 3,
    "revenue": 3,
    "guidance": 2,
    "forecast": 2,
    "upgrade": 2,
    "downgrade": 2,
    "acquisition": 3,
    "merger": 3,
    "lawsuit": 2,
    "investigation": 2,
    "AI": 4,
    "growth": 2,
}


class Ranker:
    def __init__(self, recency_lambda: float = 0.15):
        self.recency_lambda = recency_lambda

    def rank(self, docs, query: str):
        scored = []

        for doc in docs:
            score = self.score_document(doc, query)
            scored.append((doc, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [d for d, _ in scored]

    # --------------------------
    # Core scoring function
    # --------------------------

    def score_document(self, doc, query: str) -> float:
        content, metadata = self._extract(doc)
        query_lower = query.lower()

        semantic_score = self._get_semantic_score(metadata)
        keyword_score = self._keyword_score(content)
        query_score = self._query_overlap(content, query_lower)
        recency_score = self._recency_score(metadata)

        entity_boost = metadata.get("entity_boost", 0)

        final_score = (
            0.45 * semantic_score +
            0.25 * keyword_score +
            0.15 * query_score +
            0.15 * recency_score + 
            entity_boost
        )

        return final_score

    # --------------------------
    # Feature extractors
    # --------------------------

    def _extract(self, doc):
        if isinstance(doc, str):
            return doc.lower(), {}
        return getattr(doc, "page_content", "").lower(), getattr(doc, "metadata", {})

    def _get_semantic_score(self, metadata):
        """
        Expect: cosine similarity already stored from retriever
        Range: [-1, 1] or [0,1]
        """
        score = metadata.get("semantic_score", 0)

        # normalize if needed
        if score < 0:
            score = (score + 1) / 2

        return max(0.0, min(1.0, score))

    def _keyword_score(self, content: str) -> float:
        score = 0.0

        for kw, weight in IMPORTANT_KEYWORDS.items():
            if kw.lower() in content:
                score += weight

        # normalize (avoid long doc bias)
        return min(score / 10.0, 1.0)

    def _query_overlap(self, content: str, query: str) -> float:
        query_words = set(query.split())
        if not query_words:
            return 0.0

        matches = sum(1 for w in query_words if w in content)
        return matches / len(query_words)

    def _recency_score(self, metadata) -> float:
        date_field = (
            metadata.get("published_at")
            or metadata.get("date")
            or metadata.get("timestamp")
        )

        if not date_field:
            return 0.0

        try:
            doc_date = datetime.fromisoformat(date_field)
            age_days = (datetime.utcnow() - doc_date).days

            # exponential decay
            return math.exp(-self.recency_lambda * age_days)

        except Exception:
            return 0.0

    @staticmethod
    def rank_documents(docs, query):
        return Ranker().rank(docs, query)