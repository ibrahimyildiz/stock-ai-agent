import os
import chromadb
from langchain_core.documents import Document

CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = os.getenv("CHROMA_PORT", "8000")


class VectorStore:

    def __init__(self):

        self.client = chromadb.HttpClient(
            host=CHROMA_HOST,
            port=int(CHROMA_PORT)
        )

        self.collection = self.client.get_or_create_collection("stocks")

        # -------------------------
        # DOCUMENT CACHE (IMPORTANT FOR BM25)
        # -------------------------
        self._documents = []

    # =========================
    # ADD DOCUMENTS (FIXED)
    # =========================
    def add_documents(self, documents, ids, metadatas=None):

        texts = []
        final_metadatas = metadatas or []

        for doc in documents:
            texts.append(doc.page_content)
            if not metadatas:
                final_metadatas.append(doc.metadata)

        self.collection.add(
            documents=texts,
            ids=ids,
            metadatas=final_metadatas
        )

    # =========================
    # SEARCH (FIXED)
    # =========================
    def similarity_search(self, query: str, k: int = 5):

        results = self.collection.query(
            query_texts=[query],
            n_results=k
        )

        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]

        output = []

        for i in range(len(docs)):
            output.append(Document(
                page_content=docs[i],
                metadata=metas[i] if i < len(metas) else {}
            ))

        return output

    # =========================
    # BM25 SUPPORT (CRITICAL FIX)
    # =========================
    def get_all_documents(self):

        results = self.collection.get()

        docs = []

        for i in range(len(results.get("documents", []))):
            docs.append({
                "text": results["documents"][i],
                "metadata": results["metadatas"][i] if results.get("metadatas") else {}
            })

        return docs