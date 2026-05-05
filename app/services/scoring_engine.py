class ScoringEngine:

    def score(self, bull, bear):
        bull_score = len(bull) * 0.6
        bear_score = len(bear) * 0.4

        return {
            "bull_score": bull_score,
            "bear_score": bear_score
        }