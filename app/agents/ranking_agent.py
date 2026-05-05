class RankingAgent:

    def __init__(self, ranker):
        self.ranker = ranker

    async def run(self, state):

        docs = state["retrieved"]
        query = state["query"]   # 🚨 IMPORTANT FIX

        ranked_docs = self.ranker.rank(docs, query)

        return {
            "ranked": ranked_docs
        }