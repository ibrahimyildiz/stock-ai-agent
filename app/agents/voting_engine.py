class VotingEngine:

    def decide(self, bull_score, bear_score):

        if bull_score > bear_score:
            decision = "BUY"
        elif bear_score > bull_score:
            decision = "SELL"
        else:
            decision = "HOLD"

        confidence = abs(bull_score - bear_score)

        return decision, confidence