
app_tag := arxiv-admin-console
app_name := arxiv-admin-console
app_port := 4042
dockerport := 80

ROOT_DIR := $(shell pwd)
AAUTH2C_CPUS := 2
AAUTH2C_DOCKER_PLATFORM := $(shell echo $${AAUTH2C_DOCKER_PLATFORM:-linux/amd64})
# // where the auth server is running.
# export const authUrl = process.env.AAA_URL || 'http://127.0.0.1:5000/aaa';
# // where the backend is running
# export const backendUrl = process.env.ADMIN_API_BACKEND_URL || 'http://127.0.0.1:5000/api/v1'
# // and the UI is serving from
# export const appUrl = process.env.ADMIN_APP_ROOT || 'http://127.0.0.1:5000/';
RUN_HOST := https://dev3.arxiv.org
# RUN_HOST := http://127.0.0.1:5000

APP_DOCKER_RUN := docker run --cpus ${AAUTH2C_CPUS} --rm -p ${app_port}:${dockerport} \
-e PORT=${dockerport} \
-e AAA_URL=${RUN_HOST}/aaa \
-e ADMIN_API_BACKEND_URL=${RUN_HOST}/adminapi/v1 \
-e ADMIN_APP_ROOT=${RUN_HOST}/admin-console \
--name ${app_name} --security-opt="no-new-privileges=true" 

.PHONY: HELLO docker run stop

default: HELLO venv/lib/python3.12/site-packages/fastapi

HELLO:
	@echo To see the README of this Makefile, type "make help"
	@echo Local HTTP port is ${app_port}
	@echo Docker command params is:
	@echo ${APP_DOCKER_RUN}

#-#
#-# Command: help
#-#   show this message
help:
	@awk '/^#-#/ { print substr($$0, 5)}' Makefile

#-#
#-# Command: docker
#-#   builds the docker image
docker:
	@echo "PLATFORM: ${PLATFORM}"
	@echo "dockerport: ${app_port}"
	@echo "tag: ${app_tag}"
	docker buildx build -f ./Dockerfile \
                --build-arg AAA_URL=${RUN_HOST}/aaa \
                --build-arg ADMIN_API_BACKEND_URL=${RUN_HOST}/adminapi/v1 \
                --build-arg ADMIN_APP_ROOT=${RUN_HOST}/admin-console \
		--security-opt seccomp=unconfined  \
		--progress=plain \
		--platform=linux/amd64 -t ${app_tag}:latest .

#-#
#-# Command: run
#-#   runs the appliance container with the terminal attached (for test)
run: stop
	${APP_DOCKER_RUN} -it --rm ${app_tag}:latest 

#-#
#-# Command: daemon
#-#   runs the appliance container as a daemon
daemon: stop
	${APP_DOCKER_RUN} -d --rm ${app_tag}:latest 

#-#
#-# Command: stop
#-#   stops the appliance container
stop:
	-docker container kill ${app_name}
	-docker container rm ${app_name}

#-#
#-# Command: sh
#-#   runs a bash shell in the container to look inside of it
sh: stop
	${APP_DOCKER_RUN}  -it ${app_tag}:latest /bin/sh
