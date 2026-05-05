import os
import requests
import json
import re

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")


def generate_response(prompt: str, model: str = "gemma:2b"):
    response = requests.post(
        f"{OLLAMA_HOST}/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]


class OllamaClient:

    def generate(
        self,
        role: str,
        docs: list,
        query: str,
        bull=None,
        bear=None,
        model: str = "gemma:2b"
    ):

        prompt = self._build_prompt(role, docs, query, bull, bear)
        response = generate_response(prompt, model)

        return self._parse_response(response)

    def _build_prompt(self, role, docs, query, bull, bear):

        return f"""
    You are a financial judge model.

    Return ONLY valid JSON in this format:

    {{
    "decision": "buy|sell|hold",
    "confidence": 0.0-1.0,
    "agreement": 0.0-1.0
    }}

    Do not include explanations.

    QUERY:
    {query}

    BULL:
    {bull}

    BEAR:
    {bear}

    DOCUMENTS:
    {docs}
    """

    def _parse_response(self, response: str):

        # Try JSON extraction first
        try:
            return json.loads(response)
        except Exception:
            pass

        # fallback: extract structured fields from text
        decision = self._extract(response, "decision")
        confidence = self._extract(response, "confidence")
        agreement = self._extract(response, "agreement")

        return {
            "decision": decision,
            "confidence": float(confidence) if confidence else None,
            "agreement": float(agreement) if agreement else None,
            "raw": response
        }


    def _extract(self, text, key):
        match = re.search(rf"{key}\s*:\s*([^\n]+)", text)
        return match.group(1).strip() if match else None