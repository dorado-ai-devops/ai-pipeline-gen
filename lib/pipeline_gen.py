import argparse
from lib.ollama_client import OllamaClient
from lib.openai_client import OpenAIClient
from lib.utils import load_prompt

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Archivo de entrada con la descripción")
    parser.add_argument("--mode", default="ollama", choices=["ollama", "openai"], help="Modelo a utilizar")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        description = f.read().strip()

    prompt_template = load_prompt("pipeline_gen")

    full_prompt = prompt_template.replace("{{description}}", description)

    if args.mode == "ollama":
        client = OllamaClient(model="mistral")
    else:
        client = OpenAIClient()

    response = client.generate_completion(full_prompt)

    print(response)


if __name__ == "__main__":
    main()
