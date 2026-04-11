import requests

API_KEY = "9O76DAEX0X9PA7ZY"

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
        articles.append({
            "text": item["title"] + ". " + item.get("summary", ""),
            "ticker": ticker,
            "source": "alphavantage",
            "date": item.get("time_published", "")
        })

    return articles