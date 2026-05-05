class RetrievalAgent:

    def __init__(self, retriever):
        self.retriever = retriever

    async def run(self, query: str):

        docs = await self.retriever.search(query)

        return {
            "query": query,
            "documents": docs
        }