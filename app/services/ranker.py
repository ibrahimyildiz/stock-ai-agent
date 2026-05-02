from datetime import datetime

IMPORTANT_KEYWORDS = [
    "earnings",
    "revenue",
    "guidance",
    "forecast",
    "upgrade",
    "downgrade",
    "acquisition",
    "merger",
    "lawsuit",
    "investigation",
    "AI",
    "growth",
]


def score_document(doc, query: str):
    score = 0

    content = doc.page_content.lower()
    metadata = doc.metadata

    # Keyword importance
    for keyword in IMPORTANT_KEYWORDS:
        if keyword.lower() in content:
            score += 2

    # Recency
    if "date" in metadata:
        try:
            doc_date = datetime.fromisoformat(metadata["date"])
            days_old = (datetime.now() - doc_date).days

            if days_old < 1:
                score += 5
            elif days_old < 3:
                score += 3
            elif days_old < 7:
                score += 1

        except Exception:
            pass

    # Query word matching
    query_words = query.lower().split()
    matches = sum(1 for word in query_words if word in content)

    score += matches

    return score


def rank_documents(docs, query):
    scored_docs = []

    for doc in docs:
        score = score_document(doc, query)
        scored_docs.append((doc, score))

    scored_docs.sort(key=lambda x: x[1], reverse=True)

    return [doc for doc, _ in scored_docs]