from langchain_community.retrievers import BM25Retriever

from app.services.retriever import Retriever
from app.services.ranker import Ranker
from app.services.ollama_client import OllamaClient

from app.services.vector_store import VectorStore
from app.services.ingestion_service import IngestionService

from app.services.scoring_engine import ScoringEngine
from app.services.voting_engine import VotingEngine
from langchain_core.documents import Document


class Container:

    def __init__(self):

        # -------------------------
        # Core storage
        # -------------------------
        self.vector_store = VectorStore()
        self.ingestion_service = IngestionService(self.vector_store)

        # -------------------------
        # State (IMPORTANT FIX)
        # -------------------------
        self.all_documents = []
        self.bm25 = None

        # -------------------------
        # Services
        # -------------------------
        self.scoring_engine = ScoringEngine()
        self.voting_engine = VotingEngine()

        self.ranker = Ranker()
        self.llm = OllamaClient()

        # -------------------------
        # Retriever (works without BM25 initially)
        # -------------------------
        self.retriever = Retriever(
            self.vector_store,
            None  # BM25 will be attached later
        )

    # =========================
    # BUILD / REFRESH BM25
    # =========================
    def build_bm25(self):

        raw_docs = self.vector_store.get_all_documents()

        docs = []

        for d in raw_docs:

            # 🔥 normalize everything into Document
            if isinstance(d, Document):
                docs.append(d)

            elif isinstance(d, dict):
                docs.append(
                    Document(
                        page_content=d.get("page_content") or d.get("text", ""),
                        metadata=d.get("metadata", {})
                    )
                )

            else:
                # last fallback
                docs.append(
                    Document(
                        page_content=str(d),
                        metadata={}
                    )
                )

        if not docs:
            self.bm25 = None
            return

        self.bm25 = BM25Retriever.from_documents(docs)
        self.bm25.k = 20

    # =========================
    # NORMALIZATION
    # =========================
    def _normalize_docs(self, docs):
        from langchain_core.documents import Document

        normalized = []

        for d in docs:
            if isinstance(d, dict):
                normalized.append(
                    Document(
                        page_content=d.get("text") or d.get("content", ""),
                        metadata=d.get("metadata", {})
                    )
                )
            else:
                normalized.append(d)

        return normalized

    def get_all_documents(self):

        results = self.collection.get()

        docs = []

        for i in range(len(results.get("documents", []))):

            docs.append(
                Document(
                    page_content=results["documents"][i],
                    metadata=results["metadatas"][i] if results.get("metadatas") else {},
                    id=results["ids"][i] if results.get("ids") else None
                )
            )

        return docs