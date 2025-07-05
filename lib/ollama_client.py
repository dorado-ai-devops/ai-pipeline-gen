import os, json, requests

class OllamaClient:
    def __init__(self, base_url=None, model="mistral"):
        self.base = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = model

    def generate_completion(self, prompt: str) -> str:
        url = f"{self.base}/api/generate"
        payload = {"model": self.model, "prompt": prompt, "stream": False}
        resp = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
        )
        resp.raise_for_status()
        data = resp.json()
        # extrae la respuesta
        if "response" in data:
            return data["response"]
        if "choices" in data:
            return data["choices"][0]["text"]
        raise RuntimeError(f"Respuesta inesperada: {data}")
