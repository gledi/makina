# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.14

FROM python:${PYTHON_VERSION}-slim-trixie AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:${PATH}"

WORKDIR /app

RUN useradd --system --user-group --no-create-home --shell /sbin/nologin makina && \
    mkdir -p /app && chown -R makina:makina /app

USER makina

WORKDIR /app


FROM ghcr.io/astral-sh/uv:python${PYTHON_VERSION}-trixie-slim AS builder

ENV UV_COMPILE_BYTECODE=1
ENV PATH="/app/.venv/bin:${PATH}"

WORKDIR /app

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install --yes --no-install-recommends gettext && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --extra prod --no-dev --no-install-project --no-editable --link-mode=copy


FROM builder AS dev-builder

COPY . .

RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked --all-extras --all-groups --link-mode=copy


FROM builder AS prod-builder

COPY . .

RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked --extra prod --no-dev --no-editable --link-mode=copy


FROM base AS dev
COPY --from=dev-builder /app/.venv/ /app/.venv/


FROM base AS prod
ENV DJANGO_SETTINGS_MODULE=makina.core.settings.prod
COPY --from=prod-builder /app/.venv/ /app/.venv/
USER makina
CMD ["daphne", "--no-server-name", "--bind", "0.0.0.0", "--port", "8000", "makina.core.asgi:application"]
