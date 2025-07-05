# lib/openai_client.py
import os
import openai

# Configura la API key desde variable de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

class OpenAIClient:
    def __init__(self):
        if not openai.api_key:
            raise ValueError("Falta la variable de entorno OPENAI_API_KEY")

    def generate_completion(self, prompt):
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Eres un generador de pipelines DevOps a partir de descripciones de alto nivel."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1024
        )
        return response.choices[0].message.content
