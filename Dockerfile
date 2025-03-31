FROM python:3.9.21-bookworm AS builder

RUN pip install poetry==1.1.14

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --no-root

FROM python:3.9.21-slim-bookworm AS runtime

RUN pip install poetry==1.1.14

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY . ./app/

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
--mount=type=cache,target=/var/lib/apt,sharing=locked \
apt-get -y update && \
apt-get -y install --no-install-recommends \
git ffmpeg gpg nodejs mono-runtime xz-utils

ADD https://github.com/arcusmaximus/YTSubConverter/releases/download/1.6.3/YTSubConverter-Linux.tar.xz /app/ytsubconverter/a.tar.xz
RUN tar -xf /app/ytsubconverter/a.tar.xz -C /app/ytsubconverter && \
rm /app/ytsubconverter/a.tar.xz && \
apt-get purge -y --auto-remove xz-utils && \
rm -rf /var/lib/apt/lists/*

CMD ["python", "-u", "app/main.py"]