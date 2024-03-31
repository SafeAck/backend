# use chainguard hardened images with SBOM
FROM cgr.dev/chainguard/wolfi-base as builder
ARG version=3.12

WORKDIR /safeack-backend

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

# add python
RUN apk update && apk add python-${version} py${version}-pip

# install poetry
RUN python -m pip install poetry

# copy necessary files
COPY pyproject.toml poetry.lock ./

# poetry config
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

## runtime stage
FROM cgr.dev/chainguard/wolfi-base as runtime
# FROM cgr.dev/chainguard/python:latest as runtime

WORKDIR /safeack-backend
RUN chown -R nonroot.nonroot /safeack-backend && \
    mkdir -p /var/log/gunicorn && \
    chown -R nonroot.nonroot /var/log/gunicorn && \
    mkdir -p /config/ && \
    chown -R nonroot.nonroot /config

# python installation
ARG version=3.12

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

RUN apk update && apk add python-${version} py${version}-pip

# copy venv from builder image
ENV VIRTUAL_ENV=/safeack-backend/.venv \
    PATH="/safeack-backend/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# copy necessary files
COPY safeack_backend ./safeack_backend
COPY alembic ./alembic
COPY README.md alembic.ini .
COPY gunicorn.conf.py /config

USER nonroot

ENTRYPOINT ["gunicorn", "-c", "/config/gunicorn.conf.py", "safeack_backend.api:app"]
# docker run -d --rm -p 8000:8000 -v ./gunicorn-logs:/var/log/gunicorn --env-file ./.env safeack-backend

# Get shell access to container by removing ENTRYPOIN cmd line, rebuilding image again and starting shell:
# docker build . -t safeack-backend
# docker run -p 8000:8000 -v ./gunicorn-logs:/var/log/gunicorn -it --rm --env-file ./.env safeack-backend /bin/sh