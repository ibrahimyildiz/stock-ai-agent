import re
from functools import lru_cache

TICKER_MAP = {
    "nvidia": "NVDA", "nvda": "NVDA",
    "apple": "AAPL", "aapl": "AAPL",
    "microsoft": "MSFT", "msft": "MSFT",
    "google": "GOOGL", "googl": "GOOGL", "alphabet": "GOOGL",
    "amazon": "AMZN", "amzn": "AMZN",
    "tesla": "TSLA", "tsla": "TSLA",
    "meta": "META", "facebook": "META",
    "netflix": "NFLX", "nflx": "NFLX"
}

@lru_cache(maxsize=128)
def extract_ticker(query: str) -> str | None:
    """
    Extract a known stock ticker from the user query.
    Production-ready approach: uses a static map for O(1) fast lookup, 
    then falls back to an LLM extraction for any unknown companies,
    and caches the results for performance.
    """
    query_lower = query.lower()
    
    # 1. Fast Dictionary Lookup
    words = re.findall(r'\b\w+\b', query_lower)
    for word in words:
        if word in TICKER_MAP:
            return TICKER_MAP[word]
            
    for key, ticker in TICKER_MAP.items():
        if key in query_lower:
            return ticker
            
    # 2. LLM Fallback for Unknown Companies
    try:
        from app.services.ollama_client import generate_response
        prompt = (
            "You are a financial entity extractor. "
            f"Extract the stock ticker symbol from this query: '{query}'. "
            "Respond ONLY with the uppercase ticker symbol (e.g., AAPL, PLTR). "
            "If no company is mentioned, respond exactly with NONE."
        )
        llm_output = generate_response(prompt).strip().upper()
        
        if "NONE" in llm_output or not llm_output:
            return None
            
        # Clean up in case LLM added extra text
        match = re.search(r'\b[A-Z]{1,5}\b', llm_output)
        if match:
            return match.group(0)
            
    except Exception as e:
        print(f"LLM Ticker Extraction failed: {e}")
        return None

    return None
