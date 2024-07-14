# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12

FROM python:${PYTHON_VERSION}-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV VENV_DIR=/opt/venv
ENV PATH=${VENV_DIR}/bin:${PATH}

WORKDIR /app

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get upgrade --yes && \
    DEBIAN_FRONTEND=noninteractive apt-get install --yes --no-install-recommends libpq5 && \
    DEBIAN_FRONTEND=noninteractive apt-get autoremove --yes --purge && \
    DEBIAN_FRONTEND=noninteractive apt-get autoclean --yes && \
    DEBIAN_FRONTEND=noninteractive apt-get clean --yes && \
    rm -rf /var/lib/apt/lists/* && \
    useradd --system --user-group --no-create-home --shell /sbin/nologin makina


FROM python:${PYTHON_VERSION}-bookworm AS builder

ENV VENV_DIR=/opt/venv

WORKDIR /app

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get upgrade --yes && \
    DEBIAN_FRONTEND=noninteractive apt-get install --yes --no-install-recommends libpq-dev && \
    DEBIAN_FRONTEND=noninteractive apt-get autoremove --yes --purge && \
    DEBIAN_FRONTEND=noninteractive apt-get autoclean --yes && \
    DEBIAN_FRONTEND=noninteractive apt-get clean --yes && \
    rm -rf /var/lib/apt/lists/* && \
    python -m venv --prompt=makina ${VENV_DIR}

COPY . .


FROM builder AS dev-builder
RUN --mount=type=cache,target=/root/.cache/pip \
    ${VENV_DIR}/bin/python -m pip install --upgrade --upgrade-strategy=eager pip && \
    ${VENV_DIR}/bin/python -m pip install --requirement=/app/requirements/dev.txt && \
    ${VENV_DIR}/bin/python -m pip install --no-deps --editable .


FROM builder AS prod-builder
RUN --mount=type=cache,target=/root/.cache/pip \
    ${VENV_DIR}/bin/python -m pip install --upgrade --upgrade-strategy=eager pip && \
    ${VENV_DIR}/bin/python -m pip install --requirement=/app/requirements/prod.txt && \
    ${VENV_DIR}/bin/python -m pip install --no-deps .


FROM base AS dev
COPY --from=dev-builder ${VENV_DIR} ${VENV_DIR}


FROM base AS prod
ENV DJANGO_SETTINGS_MODULE=makina.core.settings.prod
COPY --from=prod-builder ${VENV_DIR}/ ${VENV_DIR}/
USER makina
CMD ["daphne", "--no-server-name", "--bind", "0.0.0.0", "--port", "8000", "makina.core.asgi:application"]
