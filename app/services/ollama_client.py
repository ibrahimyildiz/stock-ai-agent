import os
import requests

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

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