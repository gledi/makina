.PHONY: info venv list outdated tools compile compile/dry sync sync/dry install install-dev dev \
	run shellplus \
	img-dev img-prod img \
	build up svc infrastructure down destroy ps top start stop logs shell djshell

.SILENT: check venv prep-run


ARCH = $(shell uname -m)
PLATFORM =
PYENV_PREFIX = $(shell pyenv prefix 3.12)
PYENV_PYTHON_BIN = $(PYENV_PREFIX)/bin/python
VENV_DIR = $(CURDIR)/.venv
VENV_PROMPT = makina
PY = $(VENV_DIR)/bin/python
REPOSITORY = gledi/makina
SVC = web
CMD = bash

ifeq ($(ARCH),arm64)
	PLATFORM = --platform linux/amd64
endif

info:
	echo "PYENV_PREFIX =" $(PYENV_PREFIX)
	echo "PYENV_PYTHON_BIN =" $(PYENV_PYTHON_BIN)
	echo "VENV_DIR =" $(VENV_DIR)
	echo "VENV_PROMPT =" $(VENV_PROMPT)
	echo "PY =" $(PY)
	echo "REPOSITORY =" $(REPOSITORY)
	echo "TAG =" $(TAG)
	echo "SVC =" $(SVC)
	echo "CMD =" $(CMD)

t:
	@echo $(ARCH)
	@echo "PLATFORM = $(PLATFORM)"

venv:
	if ! [[ -d $(VENV_DIR) ]]; then $(PYENV_PYTHON_BIN) -m venv --prompt=$(VENV_PROMPT) $(VENV_DIR); else echo "$(VENV_DIR) already exists. skipping ..."; fi

list:
	$(PY) -m pip list

outdated:
	$(PY) -m pip list --outdated

tools:
	$(PY) -m pip install --upgrade --upgrade-strategy=eager pip pip-tools

compile:
	$(PY) -m piptools compile --no-header --allow-unsafe --resolver=backtracking --annotation-style=line --upgrade --extra=prod --output-file requirements/prod.txt
	$(PY) -m piptools compile --no-header --allow-unsafe --resolver=backtracking --annotation-style=line --upgrade --all-extras --output-file requirements/dev.txt

compile/dry:
	$(PY) -m piptools compile --dry-run --no-header --allow-unsafe --resolver=backtracking --annotation-style=line --upgrade --extra=prod --output-file requirements/prod.txt
	$(PY) -m piptools compile --dry-run --no-header --allow-unsafe --resolver=backtracking --annotation-style=line --upgrade --all-extras --output-file requirements/dev.txt

sync:
	$(PY) -m piptools sync requirements/dev.txt

sync/dry:
	$(PY) -m piptools sync --dry-run requirements/dev.txt

install:
	$(PY) -m pip install --no-deps .

install-dev:
	$(PY) -m pip install --no-deps --editable .

dev: tools compile sync install-dev

run:
	makina runserver

shellplus:
	makina shell_plus

img-dev:
	docker build $(PLATFORM) --tag $(REPOSITORY):dev --force-rm .

img-prod:
	docker build $(PLATFORM) --tag $(REPOSITORY):prod --tag $(REPOSITORY):latest --force-rm .

img: img-prod

build:
	docker compose build

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
