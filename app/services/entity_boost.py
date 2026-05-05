import re

TICKER_BOOST = 0.25
COMPANY_BOOST = 0.15


class EntityBooster:
    def boost(self, docs, query: str):
        query_upper = query.upper()

        for doc in docs:
            text = doc.page_content.upper()

            boost = 0.0

            # ticker match (AAPL, TSLA, NVDA)
            tickers = re.findall(r"\b[A-Z]{2,5}\b", query_upper)
            for t in tickers:
                if t in text:
                    boost += TICKER_BOOST

            # company name partial match
            words = query.lower().split()
            for w in words:
                if w in doc.page_content.lower():
                    boost += COMPANY_BOOST

            doc.metadata["entity_boost"] = boost

        return docs