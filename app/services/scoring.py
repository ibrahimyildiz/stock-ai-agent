def score_document(doc, query: str):
    content = doc.page_content.lower()

    score = sum(
        1 for word in query.lower().split()
        if word in content
    )

    return score


def rank_documents(docs, query: str):
    scored = []

    for doc in docs:
        score = score_document(doc, query)
        scored.append((doc, score))

    scored.sort(key=lambda x: x[1], reverse=True)

    return [d for d, _ in scored]