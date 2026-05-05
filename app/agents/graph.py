from langgraph.graph import StateGraph
from app.agents.state import GraphState
from app.core.container import Container
import json
import re

container = Container()


# =========================
# RETRIEVAL
# =========================
async def retrieval_node(state: GraphState):

    docs = container.retriever.retrieve(state["query"])

    return {
        "retrieved_docs": docs
    }


# =========================
# RANKING
# =========================
async def ranking_node(state: GraphState):

    ranked = container.ranker.rank(
        state.get("retrieved_docs", []),
        state["query"]
    )

    return {
        "ranked_docs": ranked
    }


# =========================
# BULL
# =========================
async def bull_node(state: GraphState):

    result = container.llm.generate(
        role="bull",
        docs=state.get("ranked_docs", []),
        query=state["query"]
    )

    return {
        "bull": result
    }


# =========================
# BEAR
# =========================
async def bear_node(state: GraphState):

    result = container.llm.generate(
        role="bear",
        docs=state.get("ranked_docs", []),
        query=state["query"]
    )

    return {
        "bear": result
    }


# =========================
# JUDGE (FIXED — NO QUERY MODIFICATION)
# =========================
async def judge_node(state: GraphState):

    result = container.llm.generate(
        role="judge",
        docs=state.get("ranked_docs", []),
        query=state["query"],
        bull=state.get("bull"),
        bear=state.get("bear")
    )

    return {
        "decision": result.get("decision"),
        "confidence": result.get("confidence"),
        "agreement": result.get("agreement")
    }


# =========================
# FINAL
# =========================
async def final_node(state: GraphState):

    return {
        "final_output": {
            "decision": state.get("decision"),
            "confidence": state.get("confidence"),
            "agreement": state.get("agreement"),
        }
    }


# =========================
# GRAPH
# =========================
def build_graph():

    graph = StateGraph(GraphState)

    graph.add_node("retrieval", retrieval_node)
    graph.add_node("ranking", ranking_node)
    graph.add_node("bull", bull_node)
    graph.add_node("bear", bear_node)
    graph.add_node("judge", judge_node)
    graph.add_node("final", final_node)

    graph.set_entry_point("retrieval")

    graph.add_edge("retrieval", "ranking")

    graph.add_edge("ranking", "bull")
    graph.add_edge("ranking", "bear")

    graph.add_edge("bull", "judge")
    graph.add_edge("bear", "judge")

    graph.add_edge("judge", "final")

    return graph.compile()