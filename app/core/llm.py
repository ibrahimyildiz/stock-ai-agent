# LLM wrapper (Ollama/OpenAI)

import requests

def call_llm(prompt: str):
    response = requests.post(
        "http://host.docker.internal:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]