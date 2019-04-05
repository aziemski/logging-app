DOCKER := docker
KUBECTL := kubectl
APP_IMAGE := aziemski/logging-app:latest

build:
	$(DOCKER) build -t $(APP_IMAGE) .
.PHONY: build

push:
	$(DOCKER) push $(APP_IMAGE)
.PHONY: push

release: build push
.PHONY: release

install:
	$(KUBECTL) apply -f deployment.yaml
.PHONY: install

uninstall:
	$(KUBECTL) delete -f deployment.yaml || true
.PHONY: uninstall

reinstall: uninstall install
.PHONY: reinstall
