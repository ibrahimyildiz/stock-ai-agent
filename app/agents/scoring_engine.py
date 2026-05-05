class ScoringEngine:

    def score(self, bull, bear):

        bull_score = (
            bull["signals"]["sentiment"] * 0.4 +
            bull["signals"]["growth"] * 0.4 -
            bull["signals"]["risk"] * 0.2
        )

        bear_score = (
            bear["signals"]["risk"] * 0.5 +
            (1 - bear["signals"]["sentiment"]) * 0.3 +
            (1 - bear["signals"]["growth"]) * 0.2
        )

        return bull_score, bear_score

    def agreement_score(bull_score, bear_score):
        return 1 - abs(bull_score - bear_score)