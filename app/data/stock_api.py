import requests
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

def get_stock_news(ticker: str):
    url = f"https://www.alphavantage.co/query"

    params = {
        "function": "NEWS_SENTIMENT",
        "tickers": ticker,
        "apikey": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    articles = []

    for item in data.get("feed", [])[:5]:

        raw_date = item.get("time_published", "")

        date = None
        if raw_date:
            try:
                date = datetime.strptime(raw_date, "%Y%m%dT%H%M%S").isoformat()
            except:
                date = raw_date  # fallback if format changes

        articles.append({
            "text": item["title"] + ". " + item.get("summary", ""),
            "ticker": ticker,
            "source": "alphavantage",
            "date": date
        })

    return articles