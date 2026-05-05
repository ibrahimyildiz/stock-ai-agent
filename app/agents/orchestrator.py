import asyncio

class Orchestrator:

    def __init__(
        self,
        retrieval_agent,
        ranking_agent,
        bull_agent,
        bear_agent,
        judge_agent,
        synthesis_agent
    ):
        self.retrieval_agent = retrieval_agent
        self.ranking_agent = ranking_agent
        self.bull_agent = bull_agent
        self.bear_agent = bear_agent
        self.judge_agent = judge_agent
        self.synthesis_agent = synthesis_agent

    async def run(self, query: str):

        # 1. Retrieve
        retrieved = await self.retrieval_agent.run(query)

        # 2. Rank
        ranked = await self.ranking_agent.run(retrieved)

        # 3. Parallel Debate ⚡
        bull_task = self.bull_agent.run(ranked, query)
        bear_task = self.bear_agent.run(ranked, query)

        bull_result, bear_result = await asyncio.gather(
            bull_task,
            bear_task
        )

        # 4. Judge decision
        judgment = await self.judge_agent.run(
            bull_result,
            bear_result
        )

        # 5. Final synthesis
        final = await self.synthesis_agent.run(judgment)

        return {
            "recommendation": judgment["decision"],
            "confidence": judgment["confidence"],
            "agreement": judgment["agreement"],
            "scores": {
                "bull": judgment["bull_score"],
                "bear": judgment["bear_score"]
    }
}