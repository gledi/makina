.PHONY: check venv list outdated tools compile sync install install-dev dev \
	prep-run run cleanup-containers cleanup-volumes cleanup shellplus \
	image image-prod build up down destroy ps top start stop logs shell djshell test

.SILENT: check venv prep-run

SHELL := /bin/bash

cache = 1
debug = 0

PY_VERSION = 3.12
PYENV_PREFIX = $(shell pyenv prefix $(PY_VERSION))
PYENV_PYTHON_BIN = $(PYENV_PREFIX)/bin/python
VENV_DIR = .venv
PYTHON = ./$(VENV_DIR)/bin/python
REPOSITORY = gledi/makina
TAG = develop
SVC = web
REQUIREMENTS = dev
CMD = bash

ifeq ($(cache), 0)
	NO_CACHE = --no-cache
endif


check:
	echo "PY_VERSION =" $(PY_VERSION)
	echo "PYENV_PREFIX =" $(PYENV_PREFIX)
	echo "VENV_DIR =" $(VENV_DIR)
	echo "PYENV_PYTHON_BIN =" $(PYENV_PYTHON_BIN)
	echo "REPOSITORY =" $(REPOSITORY)
	echo "TAG =" $(TAG)
	echo "SVC =" $(SVC)
	echo "CMD =" $(CMD)
	echo "NO_CACHE =" $(NO_CACHE)
	echo "REQUIREMENTS =" $(REQUIREMENTS)

venv:
	if ! [[ -d $(VENV_DIR) ]]; then $(PYENV_PYTHON_BIN) -m venv --prompt=makina $(VENV_DIR); else echo "$(VENV_DIR) already exists. skipping ..."; fi

list:
	$(PYTHON) -m pip list

outdated:
	$(PYTHON) -m pip list --outdated

tools:
	$(PYTHON) -m pip install --upgrade --upgrade-strategy=eager pip setuptools wheel pip-tools

compile:
	$(PYTHON) -m piptools compile --resolver=backtracking --upgrade --extra=prod --output-file requirements/prod.txt
	$(PYTHON) -m piptools compile --resolver=backtracking --upgrade --all-extras --output-file requirements/dev.txt

sync:
	$(PYTHON) -m piptools sync requirements/$(REQUIREMENTS).txt

install:
	$(PYTHON) -m pip install --no-deps .

install-dev:
	$(PYTHON) -m pip install --no-deps --editable '.[dev]'

dev: tools compile sync install-dev

prep-run:
	if [[ "$(shell docker ps -aq --filter name=makina-cache)" != "" ]]; then \
		docker rm -f makina-cache; \
	fi
	if [[ "$(shell docker ps -aq --filter name=makina-db)" != "" ]]; then \
		docker rm -f makina-db; \
	fi
	if [[ "$(shell docker volume ls --filter name=makina-dbdata)" == "" ]]; then \
		docker volume create makina-dbdata; \
	fi
	docker run --rm --name=makina-cache -p 6379:6379 -d redis:7.2-alpine
	docker run --rm --name=makina-db -p 5432:5432 -v makina-dbdata:/var/lib/postgresql/data -e PGTZ=UTC -e POSTGRES_USER=makina -e POSTGRES_PASSWORD=anikam -e POSTGRES_DB=makina -d postgres:16-alpine

run:
	makina runserver

cleanup-containers:
	docker stop makina-cache makina-db

cleanup-volumes:
	docker volume rm makina-dbdata

cleanup: cleanup-containers cleanup-volumes

shellplus:
	makina shell_plus

image:
	docker build --tag $(REPOSITORY):$(TAG) --force-rm $(NO_CACHE) .

image-prod:
	docker build --tag $(REPOSITORY):prod --tag $(REPOSITORY):latest --force-rm $(NO_CACHE) .

build:
	docker compose build $(NO_CACHE)

up:
	docker compose up --build -d

down:
	docker compose down --remove-orphans --rmi local

destroy:
	docker compose down --remove-orphans --rmi local --volumes

ps:
	docker compose ps

top:
	docker compose top $(SVC)

start:
	docker compose start $(SVC)

stop:
	docker compose stop $(SVC)

logs:
	docker compose logs -f $(SVC)

shell:
	docker compose exec $(SVC) $(CMD)

djshell:
	docker compose exec web python manage.py shell_plus

test:
	docker compose run --rm web python -m pytest -v
