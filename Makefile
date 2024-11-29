.PHONY: help version \
	venv list outdated tools compile compile/dry sync sync/dry install install-dev dev \
	lint watch fix format \
	run shellplus \
	img-dev img-prod img \
	build up up/debug svc infrastructure down destroy ps top stats start stop logs shell djshell

.SILENT: help version venv

.DEFAULT_GOAL := help


ARCH := $(shell uname -m)
PLATFORM :=
PY_VERSION := 3.13
PYENV_PREFIX := $(shell pyenv prefix $(PY_VERSION))
PYENV_PYTHON_BIN := $(PYENV_PREFIX)/bin/python
VENV_DIR := $(CURDIR)/.venv
VENV_PROMPT := makina
PY := $(VENV_DIR)/bin/python
REPOSITORY := gledi/makina

PROFILES := --profile app --profile infrastructure

ifeq ($(ARCH),arm64)
	PLATFORM = --platform linux/amd64
endif

help:
	echo "Usage: make [target]"
	echo ""
	echo "Targets:"
	echo "  info:        Show various variables used in the Makefile"
	echo ""
	echo "  venv:        Create virtual environment"
	echo "  list:        List installed packages"
	echo "  outdated:    List outdated packages"
	echo "  tools:       Install pip-tools"
	echo "  compile:     Compile requirements"
	echo "  compile/dry: Dry-run compile requirements"
	echo "  sync:        Sync requirements"
	echo "  sync/dry:    Dry-run sync requirements"
	echo "  install:     Install package"
	echo "  install-dev: Install package in editable mode"
	echo "  dev:         Prepare package for development"
	echo ""
	echo "  lint:        Lint code using ruff"
	echo "  watch:       Watch code using ruff"
	echo "  fix:         Fix code using ruff"
	echo "  format:      Format code using ruff"
	echo ""
	echo "  run:         Run development server"
	echo "  shellplus:   Enter django's interactive shell"
	echo ""
	echo "  img-dev:     Build docker image for development"
	echo "  img-prod:    Build docker image for production"
	echo "  img:         Build docker image for production"
	echo ""
	echo "  build:       Build docker compose services"
	echo "  up:          Start docker compose services"
	echo "  up/debug:    Start docker compose services where our app is debuggable"
	echo "  svc:         Start a specific docker compose service"
	echo "  infra infrastructure: Start docker compose services for infrastructure (db, cache, etc.)"
	echo "  down:        Stop and remove docker compose services"
	echo "  destroy:     Stop and remove docker compose services with volumes"
	echo "  ps:          List docker compose services"
	echo "  top:         Display the running processes of docker compose service(s)"
	echo "  start:       Start a docker compose service"
	echo "  stop:        Stop a docker compose service"
	echo "  restart:     Restart a docker compose service"
	echo "  logs:        Show logs of a docker compose service"
	echo "  shell:       Enter a docker compose service"
	echo "  djshell:     Enter django's interactive shell running in a docker compose service"

print-% : ; @echo $* = $($*)

version:
	$(PY) --version
	$(PY) -c "import sys; print('GIL?', sys._is_gil_enabled())"
	echo -n "makina "
	$(PY) -m makina --version

venv:
	if ! [[ -d $(VENV_DIR) ]]; then $(PYENV_PYTHON_BIN) -m venv --prompt=$(VENV_PROMPT) $(VENV_DIR); else echo "$(VENV_DIR) already exists. skipping ..."; fi

list:
	$(PY) -m pip list

outdated:
	$(PY) -m pip list --outdated

tools:
	$(PY) -m pip install --upgrade --upgrade-strategy=eager pip pip-tools

compile:
	$(PY) -m piptools compile --no-header --allow-unsafe --resolver=backtracking --annotation-style=line --strip-extras --upgrade --extra=prod --output-file requirements/prod.txt
	$(PY) -m piptools compile --no-header --allow-unsafe --resolver=backtracking --annotation-style=line --strip-extras --upgrade --all-extras --output-file requirements/dev.txt

compile/dry:
	$(PY) -m piptools compile --dry-run --no-header --allow-unsafe --resolver=backtracking --annotation-style=line --strip-extras --upgrade --extra=prod --output-file requirements/prod.txt
	$(PY) -m piptools compile --dry-run --no-header --allow-unsafe --resolver=backtracking --annotation-style=line --strip-extras --upgrade --all-extras --output-file requirements/dev.txt

sync:
	$(PY) -m piptools sync requirements/dev.txt

sync/dry:
	$(PY) -m piptools sync --dry-run requirements/dev.txt

install:
	$(PY) -m pip install --no-deps .

install-dev:
	$(PY) -m pip install --no-deps --editable .

dev: tools compile sync install-dev


lint:
	$(PY) -m ruff check --preview ./src

watch:
	$(PY) -m ruff check --watch ./src

fix:
	$(PY) -m ruff --fix ./src

format:
	$(PY) -m ruff format ./src


run:
	makina runserver

shellplus:
	makina shell_plus


img-dev:
	docker build $(PLATFORM) --tag $(REPOSITORY):dev --force-rm --target dev .

img-prod:
	docker build $(PLATFORM) --tag $(REPOSITORY):prod --tag $(REPOSITORY):latest --force-rm .

img: img-prod


build:
	docker compose $(PROFILES) build --parallel

up:
	docker compose $(PROFILES)  up --build -d

up/debug:
	docker compose $(PROFILES) --file compose.yml --file compose.debug.yml up -d

svc:
	docker compose $(PROFILES) up --build -d $(if $(filter-out $@,$(MAKECMDGOALS)), $(filter-out $@,$(MAKECMDGOALS)), app)

infrastructure:
	docker compose --profile infrastructure up -d

down:
	docker compose $(PROFILES) down --remove-orphans --rmi local

destroy:
	docker compose $(PROFILES) down --remove-orphans --rmi local --volumes

ps:
	docker compose $(PROFILES) ps --all

top:
	docker compose $(PROFILES) top

stats:
	docker compose $(PROFILES) stats

start:
	docker compose $(PROFILES) start $(if $(filter-out $@,$(MAKECMDGOALS)), $(filter-out $@,$(MAKECMDGOALS)), app)

stop:
	docker compose $(PROFILES) stop $(if $(filter-out $@,$(MAKECMDGOALS)), $(filter-out $@,$(MAKECMDGOALS)), app)

restart:
	docker compose $(PROFILES) restart $(if $(filter-out $@,$(MAKECMDGOALS)), $(filter-out $@,$(MAKECMDGOALS)), app)

logs:
	docker compose $(PROFILES) logs -f $(if $(filter-out $@,$(MAKECMDGOALS)), $(filter-out $@,$(MAKECMDGOALS)), app)

shell:
	docker compose $(PROFILES) exec $(if $(filter-out $@,$(MAKECMDGOALS)), $(filter-out $@,$(MAKECMDGOALS)), app) bash

djshell:
	docker compose $(PROFILES) exec app makina shell_plus

%:
	@:
