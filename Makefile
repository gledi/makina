.DEFAULT_GOAL := help

SHELL := /bin/bash

PROJECTNAME := $(shell basename $(CURDIR))
PACKAGE_NAME := $(PROJECTNAME)

PY_VERSION := 3.14
VENV_DIR := $(CURDIR)/.venv
VENV_PROMPT := $(PROJECTNAME)-$(PY_VERSION)

PY := $(VENV_DIR)/bin/python
UV := $(shell which uv 2>/dev/null || echo "uv")

IMAGE_NAME := gledi/$(PROJECTNAME)

CMD := /bin/bash

PROFILES := --profile app --profile infrastructure


.PHONY: help print-%
.SILENT: help print-%

help: ## Show this help message and exit
	echo ""
	echo "Manage $(PROJECTNAME). Usage:"
	echo ""
	grep -E '^[a-zA-Z_/%-]+( [a-zA-Z_/%-]+)*:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36mmake %-28s\033[0m %s\n", $$1, $$2}'
	echo ""

print-% : ; @echo $* = $($*)


.PHONY: venv list outdated lock lock/check sync sync/dry deptree
.SILENT: venv

venv: ## Create a virtual environment
	if ! [[ -d $(VENV_DIR) ]]; then \
		uv venv --no-project --seed --link-mode=copy --prompt=$(VENV_PROMPT) $(VENV_DIR) --python=$(PY_VERSION); \
	else \
		echo "Virtual environment already exists"; \
	fi

list: ## List all dependencies
	$(UV) pip list

outdated: ## List outdated dependencies
	$(UV) pip list --outdated

lock: ## Lock dependencies (uv lock --upgrade)
	$(UV) lock --refresh --upgrade --resolution=highest

lock/check: ## Check lockfile is up-to-date
	$(UV) lock --check

sync: ## Sync dependencies from lockfile
	$(UV) sync --locked --all-extras --all-groups --link-mode=copy

sync/dry: ## Dry run of syncing dependencies from lockfile
	$(UV) sync --locked --all-extras --all-groups --link-mode=copy --dry-run

deptree: ## Show dependency tree
	$(UV) tree --outdated


.PHONY: version build clean dev
.SILENT: version clean

version: ## Show Python, uv and package versions
	$(UV) run --locked python --version
	$(UV) --version
	$(UV) run --locked python -c "from importlib.metadata import version; print('$(PACKAGE_NAME)', version('$(PACKAGE_NAME)'))"

build: ## Build the package
	$(UV) build

clean: ## Remove build artifacts and caches
	rm -rf dist/ build/
	rm -rf .pytest_cache/ .ruff_cache/ .nox/
	find . -path ./.venv -prune -o -type d -name '*.egg-info' -print -exec rm -rf {} +
	find .unitreports -mindepth 1 ! -name .gitkeep -delete
	find . -path ./.venv -prune -o -type d -name __pycache__ -print -exec rm -rf {} +

dev: venv lock sync ## Prepare development environment (create venv, lock dependencies, sync from lockfile)

.PHONY: image image/prod image/dev

image image/prod: ## Build Production Docker Image
	docker buildx build --target prod --tag $(IMAGE_NAME):latest --tag $(IMAGE_NAME):prod .

image/dev: ## Build Development Docker Image
	docker buildx build --target dev --tag $(IMAGE_NAME):dev .


.PHONY: up build/compose up/build up/debug down destroy infra infrastructure

up: ## Run all services in all profiles
	docker compose $(PROFILES) up -d

build/compose: ## Build all services in all profiles
	docker compose $(PROFILES) build

up/build: ## Run all services in all profiles and force build them
	docker compose $(PROFILES) up -d --build

up/debug: ## Run all services in all profiles (app will start in debug mode)
	docker compose --file compose.yml --file compose.debug.yml $(PROFILES) up -d

down: ## Stop and remove all services in all profiles
	docker compose $(PROFILES) down --remove-orphans

destroy: ## Stop all services, remove volumes and orphans
	docker compose $(PROFILES) down --volumes --remove-orphans

infra infrastructure: ## Run infrastructure services
	docker compose --profile infrastructure up -d


%:
	@:
