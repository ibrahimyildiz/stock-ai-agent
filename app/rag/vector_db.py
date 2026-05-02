import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection("stock_news")


def add_documents(texts, metadatas, ids):
    collection.add(
        documents=texts,
        metadatas=metadatas,
        ids=ids
    )

def query_documents(query, ticker=None, n_results=5):
    if ticker:
        return collection.query(
            query_texts=[query],
            n_results=n_results,
            where={"ticker": ticker}   # 🔥 THIS IS THE FIX
        )
    else:
        return collection.query(
            query_texts=[query],
            n_results=n_results
        )