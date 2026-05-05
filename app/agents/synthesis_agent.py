class SynthesisAgent:

    async def run(self, judgment):

        return {
            "recommendation": judgment["final_decision"],
            "confidence": judgment["confidence"]
        }