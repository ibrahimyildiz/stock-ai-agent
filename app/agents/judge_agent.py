class JudgeAgent:

    def __init__(self, llm):
        self.llm = llm

    async def run(self, bull, bear):

        # simple rule-based decision for now
        if len(bull) > len(bear):
            return {
                "decision": "BUY",
                "confidence": 0.7,
                "agreement": 0.6,
                "bull_score": len(bull),
                "bear_score": len(bear),
            }

        return {
            "decision": "SELL",
            "confidence": 0.6,
            "agreement": 0.5,
            "bull_score": len(bull),
            "bear_score": len(bear),
        }