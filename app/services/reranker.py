class LLMReranker:
    def __init__(self, llm):
        self.llm = llm

    async def rerank(self, query: str, docs: list, top_k: int = 10):
        prompt = self._build_prompt(query, docs[:top_k])

        response = await self.llm.ainvoke(prompt)

        order = self._parse(response)

        return [docs[i] for i in order]

    def _build_prompt(self, query, docs):
        text = f"""
You are a financial relevance ranking system.

Query: {query}

Rank these documents by relevance to investment decision:

"""

        for i, doc in enumerate(docs):
            text += f"\n[{i}] {doc.page_content[:300]}"

        text += "\nReturn JSON list of indices sorted best to worst."

        return text

    def _parse(self, response):
        try:
            import json
            return json.loads(response)
        except:
            return list(range(len(response)))