import requests
OLLAMA_URL = "http://host.docker.internal:11434/api/generate"

def llm_generate(prompt: str):
    import requests

    res = requests.post(
        OLLAMA_URL,
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return res.json()["response"]