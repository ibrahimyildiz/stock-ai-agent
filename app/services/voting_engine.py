class VotingEngine:

    def decide(self, bull_score, bear_score):

        if bull_score > bear_score:
            return "BUY"
        elif bear_score > bull_score:
            return "SELL"
        else:
            return "HOLD"