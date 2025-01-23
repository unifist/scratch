ACCOUNT=gaf3
IMAGE=unifist-unum-scratch
VERSION?=0.0.4
DEBUG_PORT=16738
TTY=$(shell if tty -s; then echo "-it"; fi)
VOLUMES=-v ${PWD}/bin/:/opt/service/bin/ \
        -v ${PWD}/lib/:/opt/service/lib/ \
        -v ${PWD}/config/:/opt/service/config/ \
        -v ${PWD}/secret/:/opt/service/secret/
ENVIRONMENT=-e test="python -m unittest -v " \
			-e debug="python -m ptvsd --host 0.0.0.0 --port 5678 --wait -m unittest -v " \
			-e PYTHONDONTWRITEBYTECODE=1 \
			-e PYTHONUNBUFFERED=1
CLUSTER=do-nyc2-unifist-dev-nyc2
APP=scratch


.PHONY: zip unzip secret config build shell post basesheet ohsheet sheetpost hello shouldi outreach draft deploy-hello deploy-shouldi deploy-needsheet

zip:
	zip secret.zip secret/*

unzip:
	unzip secret.zip

secret:
	kubectl --context $(CLUSTER) create secret generic secret -n $(APP) --save-config --dry-run=client \
	--from-file=secret/bsky.json \
	--from-file=secret/discord.json \
	--from-file=secret/gcloud.json \
	--from-file=secret/github.json \
	--from-file=secret/zoom.json \
	-o yaml | kubectl apply -f -

config:
	kubectl --context $(CLUSTER) create configmap config -n $(APP) --save-config --dry-run=client \
	--from-file=config/outreach.json \
	-o yaml | kubectl apply -f -

build:
	docker build . -t $(ACCOUNT)/$(IMAGE):$(VERSION)

push:
	docker push $(ACCOUNT)/$(IMAGE):$(VERSION)

shell:
	-docker run $(TTY) --rm $(VOLUMES) $(ENVIRONMENT) -p 127.0.0.1:$(DEBUG_PORT):5678 $(ACCOUNT)/$(IMAGE):$(VERSION) sh

post:
	docker run $(TTY) $(VOLUMES) $(ENVIRONMENT) $(ACCOUNT)/$(IMAGE):$(VERSION) sh -c "bin/post.py"

basesheet:
	docker run $(TTY) $(VOLUMES) $(ENVIRONMENT) $(ACCOUNT)/$(IMAGE):$(VERSION) sh -c "bin/basesheet.py"

ohsheet:
	docker run $(TTY) $(VOLUMES) $(ENVIRONMENT) $(ACCOUNT)/$(IMAGE):$(VERSION) sh -c "bin/ohsheet.py"

sheetpost:
	docker run $(TTY) $(VOLUMES) $(ENVIRONMENT) $(ACCOUNT))/$(IMAGE):$(VERSION) sh -c "bin/sheetpost.py"

hello:
	docker run $(TTY) $(VOLUMES) $(ENVIRONMENT) $(ACCOUNT)/$(IMAGE):$(VERSION) sh -c "bin/hello.py"

shouldi:
	docker run $(TTY) $(VOLUMES) $(ENVIRONMENT) $(ACCOUNT)/$(IMAGE):$(VERSION) sh -c "bin/shouldi.py"

draft:
	docker run $(TTY) $(VOLUMES) $(ENVIRONMENT) $(ACCOUNT)/$(IMAGE):$(VERSION) sh -c "bin/draft.py"

needsheet:
	docker run $(TTY) $(VOLUMES) $(ENVIRONMENT) $(ACCOUNT)/$(IMAGE):$(VERSION) sh -c "bin/needsheet.py"

deploy-hello:
	kubectl --context $(CLUSTER) apply -f deployments/hello.yaml

deploy-shouldi:
	kubectl --context $(CLUSTER) apply -f deployments/shouldi.yaml

deploy-needsheet:
	kubectl --context $(CLUSTER) apply -f deployments/needsheet.yaml
