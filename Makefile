IMAGE_NAME     := ai-pipeline-gen
VERSION        := v1.0.1
REGISTRY       := localhost:5000
HELM_VALUES    := ../devops-ai-lab/manifests/helm-pipeline-gen/values.yaml
ARGO_APP_NAME  := pipeline-gen

.PHONY: all build tag push update-values sync release run

all: release

build:
	docker build --no-cache -t $(IMAGE_NAME):$(VERSION) .

tag: build
	docker tag $(IMAGE_NAME):$(VERSION) $(REGISTRY)/$(IMAGE_NAME):$(VERSION)

push: tag
	docker push $(REGISTRY)/$(IMAGE_NAME):$(VERSION)

update-values:
	@echo "Actualizando Helm values para $(IMAGE_NAME)…"
	# Actualiza el repositorio
	sed -i "s|^\(\s*repository:\s*\).*|\1$(REGISTRY)/$(IMAGE_NAME)|" $(HELM_VALUES)
	# Actualiza la versión (tag)
	sed -i "s|^\(\s*tag:\s*\).*|\1\"$(VERSION)\"|"           $(HELM_VALUES)

sync:
	@echo "Sincronizando ArgoCD (app: $(ARGO_APP_NAME))…"
	argocd app sync $(ARGO_APP_NAME)

release: push update-values sync
	@echo "Release completo: $(REGISTRY)/$(IMAGE_NAME):$(VERSION) desplegado y sincronizado con ArgoCD."

run:
	docker run -p 5003:5003 $(REGISTRY)/$(IMAGE_NAME):$(VERSION)
