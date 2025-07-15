# ⚙️ ai-pipeline-gen

> Microservicio generador de pipelines CI/CD a partir de descripciones textuales, impulsado por modelos de lenguaje como GPT-4o (OpenAI) u Ollama (LLaMA3, Phi-3, etc). Recibe una descripción de alto nivel y devuelve un pipeline YAML funcional en formato Jenkins declarativo.

---

## 🚀 Funcionalidades

- 🛠️ Genera pipelines CI/CD a partir de texto natural
- 🧠 Soporta OpenAI GPT-4o y modelos locales vía Ollama
- 🔌 Expone microservicio Flask con endpoint `/generate`
- 📦 CLI compatible para ejecución local
- 📄 Prompts modulares editables (`pipeline_gen.prompt`)
- 🐳 Contenedor listo para despliegue en Kubernetes
- 🔁 Integrable con `ai-gateway` como backend IA centralizado

---

## 📦 Estructura del Proyecto


```
ai-pipeline-gen/
├── app.py                  # Microservicio Flask (API /generate)
├── lib/                    # Clientes IA + lógica principal
│   ├── ollama_client.py
│   ├── openai_client.py
│   ├── pipeline_gen.py     # Punto de entrada CLI
│   └── utils.py
├── prompts/
│   └── pipeline_gen.prompt # Plantilla de prompt para generación
├── run.sh                  # Lanzador simple
├── Makefile                # Build/despliegue automatizado
├── Dockerfile              # Imagen del microservicio
├── requirements.txt        # Dependencias Python
└── README.md               # Documentación del proyecto
```

---

## 🔍 Descripción de Componentes

### `app.py`

Microservicio Flask que expone `/generate`.  
- Entrada esperada:
```json
{
  "description": "Pipeline básico con test y deploy",
  "mode": "ollama" // o "openai"
}
```
- Devuelve un YAML generado en respuesta.

### `lib/pipeline_gen.py`

Entrada CLI para uso local.  
Acepta archivo `.txt` como input con la descripción del pipeline.  
Ejemplo:
```bash
python3 lib/pipeline_gen.py --input mydesc.txt --mode openai
```

### `lib/openai_client.py` y `lib/ollama_client.py`

- Clientes independientes para cada backend.
- Soportan inferencia vía API externa (`openai`) o local (`ollama`).
- Se seleccionan desde la CLI o el payload JSON.

### `prompts/pipeline_gen.prompt`

Prompt dinámico con la variable `{{description}}` que será sustituida por la entrada del usuario.

---

## 🐳 Docker

```bash
docker build -t ai-pipeline-gen:dev .
docker run -p 5003:5003 ai-pipeline-gen:dev
```

---

## 🛠️ Makefile

Tareas útiles disponibles:

```bash
make build              # Construye la imagen
make load               # Carga en KIND local
make update-values      # Refresca values.yaml (Helm)
make sync               # Sincroniza con ArgoCD
make release VERSION=vX.Y.Z  # Build completo + despliegue
```

---

## 🌐 Integración con ai-gateway

Se espera que el servicio esté accesible internamente en Kubernetes en la siguiente dirección:

```
http://pipeline-gen-service.devops-ai.svc.cluster.local:80/generate
```

Y el `ai-gateway` reenvía peticiones como:

```json
{
  "description": "Pipeline de build y despliegue con validaciones Helm",
  "mode": "ollama"
}
```

---

## 🧪 Ejemplo de salida

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

## 🧠 Inspirado por

- [OpenAI API](https://platform.openai.com)
- [Ollama](https://ollama.com)
- [Jenkins Pipelines](https://www.jenkins.io/doc/book/pipeline/)

---

## 👨‍💻 Autor

- **Dani** — [@dorado-ai-devops](https://github.com/dorado-ai-devops)

---

## 🛡️ Licencia

Licencia Pública General GNU v3.0
