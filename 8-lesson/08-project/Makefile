# Используется синтаксис gnu make
# MacOs: brew install make, далее используйте gmake
# Windows: choco install make
#
.PHONY: help
.ONESHELL:

export DOCKER_APP_PORT ?= 8000

$(shell [ ! -f .env ] && cp .env.example .env)

include .env
export $(shell sed 's/=.*//' .env)

# COLORS
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)


TARGET_MAX_CHAR_NUM=20
# Это сообщение
help:
	@echo ''
	@echo 'Используется синтаксис gnu make'
	@echo 'MacOs: brew install make, далее используйте gmake'
	@echo 'Windows: choco install make'
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		helpMessage = match(lastLine, /^# (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 2, RLENGTH); \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)

PWD=$(shell pwd)
PROJECT?=project_example
export COMPOSE_PROJECT_NAME?=$(PROJECT)

COMPOSE_CMD=docker compose -p $(COMPOSE_PROJECT_NAME)
COMPOSE_EXEC=$(COMPOSE_CMD) exec -T app /bin/bash -c
COMPOSE_STOP_ALL=$(COMPOSE_CMD) stop
IN_DOCKER?=1

ifeq ($(IN_DOCKER), 1)
	RUNNER=-$(COMPOSE_CMD) run --rm app /bin/bash -c

	NO_TTY?=0
	ifeq ($(NO_TTY),1)
	RUNNER=$(COMPOSE_CMD) run --no-TTY --rm app /bin/bash -c
	endif

else
	RUNNER=
	COMPOSE_STOP_ALL=
endif

# старт приложения со сборкой
build:
	$(COMPOSE_CMD) build

# старт приложения со сборкой
run:
	$(COMPOSE_CMD) up --build

# запуск тестов в сi
test:
	-$(RUNNER) pytest tests

# запуск шела в не запущенном контейнере т.е. без авто старта других сервисов
shell-tmp:
	$(COMPOSE_CMD) run --rm app bash
	$(COMPOSE_STOP_ALL)


