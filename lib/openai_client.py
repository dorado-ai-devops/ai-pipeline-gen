# lib/openai_client.py
import openai

class OpenAIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key

    def generate_completion(self, prompt):
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Eres un analizador de logs DevOps. Devuelve diagnóstico y recomendaciones."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1024
        )
        return response.choices[0].message.content
