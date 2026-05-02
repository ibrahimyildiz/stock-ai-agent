import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection("stock_news")


def add_documents(texts, metadatas, ids):
    collection.add(
        documents=texts,
        metadatas=metadatas,
        ids=ids
    )

def query_documents(query, ticker=None):

    query_params = {
        "query_texts": [query],
        "n_results": 5
    }

    # Apply metadata filter
    if ticker:
        query_params["where"] = {
            "ticker": ticker
        }

    return collection.query(**query_params)