from typing import TypedDict, List, Any, Optional


class AgentOutput(TypedDict, total=False):
    text: str
    reasoning: str
    score: float


class GraphState(TypedDict, total=False):

    # -------------------------
    # INPUT
    # -------------------------
    query: str

    # -------------------------
    # RETRIEVAL LAYER
    # -------------------------
    retrieved_docs: List[Any]
    ranked_docs: List[Any]

    # -------------------------
    # AGENTS
    # -------------------------
    bull: AgentOutput
    bear: AgentOutput

    # -------------------------
    # DECISION LAYER
    # -------------------------
    decision: str
    confidence: float
    agreement: float

    # -------------------------
    # OPTIONAL SCORING
    # -------------------------
    bull_score: Optional[float]
    bear_score: Optional[float]

    # -------------------------
    # OUTPUT
    # -------------------------
    final_output: dict