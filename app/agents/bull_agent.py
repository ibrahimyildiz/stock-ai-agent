import json

class BullAgent:

    def __init__(self, llm):
        self.llm = llm

    async def run(self, ranked_data, query: str):

        prompt = f"""
You are a bullish financial analyst.

User Query: {query}

Market Data:
{ranked_data}

Argue why this stock is a GOOD investment.

Focus on:
- growth
- positive signals
- upside potential

IMPORTANT:
Return JSON ONLY.

{{
  "analysis": "...",
  "signals": {{
    "sentiment": 0-1,
    "growth": 0-1,
    "risk": 0-1
  }},
  "confidence": 0-1
}}
"""
        response = await self.llm.generate(prompt)

        try:
            parsed = json.loads(response)
        except Exception:
            parsed = {
                "analysis": response,
                "signals": {
                    "sentiment": 0.5,
                    "growth": 0.5,
                    "risk": 0.5
                },
                "confidence": 0.5
            }

        return parsed