from langchain.schema import Document


def normalize_documents(docs):
    normalized = []

    for doc in docs:
        if isinstance(doc, Document):
            normalized.append(doc)

        elif isinstance(doc, str):
            normalized.append(Document(page_content=doc, metadata={}))

        elif isinstance(doc, dict):
            normalized.append(
                Document(
                    page_content=doc.get("content", ""),
                    metadata=doc.get("metadata", {})
                )
            )

    return normalized