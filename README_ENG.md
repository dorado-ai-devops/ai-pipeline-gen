# ⚙️ ai-pipeline-gen

> CI/CD pipeline generator microservice powered by language models like GPT-4o (OpenAI) or Ollama (LLaMA3, Phi-3, etc). It receives a high-level description and returns a functional declarative Jenkins YAML pipeline.

---

## 🚀 Features

- 🛠️ Generates CI/CD pipelines from natural language
- 🧠 Supports OpenAI GPT-4o and local models via Ollama
- 🔌 Flask microservice with `/generate` endpoint
- 📦 CLI compatible for local execution
- 📄 Editable modular prompts (`pipeline_gen.prompt`)
- 🐳 Docker-ready for Kubernetes deployment
- 🔁 Integrates with `ai-gateway` as centralized AI backend

---

## 📦 Project Structure

```
ai-pipeline-gen/
├── app.py                  # Flask microservice (API /generate)
├── lib/                    # AI clients + core logic
│   ├── ollama_client.py
│   ├── openai_client.py
│   ├── pipeline_gen.py     # CLI entry point
│   └── utils.py
├── prompts/
│   └── pipeline_gen.prompt # Prompt template for generation
├── run.sh                  # Simple launcher
├── Makefile                # Automated build/deploy
├── Dockerfile              # Microservice image
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## 🔍 Component Breakdown

### `app.py`

Flask microservice exposing `/generate`.

- Expected input:
```json
{
  "description": "Basic pipeline with test and deploy",
  "mode": "ollama" // or "openai"
}
```
- Returns generated Jenkins YAML.

### `lib/pipeline_gen.py`

CLI entry point for local usage.  
Accepts `.txt` file as input with the pipeline description.

Example:
```bash
python3 lib/pipeline_gen.py --input mydesc.txt --mode openai
```

### `lib/openai_client.py` and `lib/ollama_client.py`

- Dedicated clients for each backend.
- Support inference via remote (`openai`) or local (`ollama`) API.
- Mode is selected via CLI or JSON payload.

### `prompts/pipeline_gen.prompt`

Dynamic prompt template with `{{description}}` placeholder for user input.

---

## 🐳 Docker

```bash
docker build -t ai-pipeline-gen:dev .
docker run -p 5003:5003 ai-pipeline-gen:dev
```

---

## 🛠️ Makefile

Available tasks:

```bash
make build              # Build Docker image
make load               # Load into local KIND cluster
make update-values      # Refresh values.yaml (Helm)
make sync               # Sync with ArgoCD
make release VERSION=vX.Y.Z  # Full release pipeline
```

---

## 🌐 ai-gateway Integration

Service is expected to be available at:

```
http://pipeline-gen-service.devops-ai.svc.cluster.local:80/generate
```

And the `ai-gateway` forwards requests like:

```json
{
  "description": "Build and deploy pipeline with Helm validations",
  "mode": "ollama"
}
```

---

## 🧪 Sample Output

```groovy
pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh 'make build'
      }
    }
    stage('Test') {
      steps {
        sh 'pytest tests/'
      }
    }
    stage('Deploy') {
      steps {
        sh './deploy.sh'
      }
    }
  }
}
```

---

## 🧠 Inspired by

- [OpenAI API](https://platform.openai.com)
- [Ollama](https://ollama.com)
- [Jenkins Pipelines](https://www.jenkins.io/doc/book/pipeline/)

---

## 👨‍💻 Author

- **Dani** — [@dorado-ai-devops](https://github.com/dorado-ai-devops)

---

## 🛡️ License

GNU General Public License v3.0