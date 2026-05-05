class ReasoningAgent:

    def __init__(self, llm):
        self.llm = llm

    async def run(self, ranked_data, query: str):

        prompt = f"""
You are a financial reasoning AI.

User Query: {query}

Top Market Data:
{ranked_data}

Analyze:
- sentiment
- risk level
- investment logic
- key signals

Return structured reasoning.
"""

        response = await self.llm.generate(prompt)

        return {
            "analysis": response,
            "confidence": 0.75
        }