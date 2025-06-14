##################################################
#                  Builder                       #
##################################################

FROM python:3.12.8-alpine AS builder

WORKDIR /code

RUN apk update --no-cache && apk upgrade --no-cache --available

# hadolint ignore=DL3018
RUN apk --no-cache update && apk --no-cache add musl-dev libpq-dev gcc g++

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# hadolint ignore=DL3059
RUN uv python pin 3.12.8

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

COPY pyproject.toml uv.lock /code/

RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked

##################################################
#                  Runtime                       #
##################################################

FROM python:3.12.8-alpine

WORKDIR /code

ENV PATH="/code/.venv/bin:$PATH"

# hadolint ignore=DL3018
RUN apk --no-cache update && apk --no-cache add libpq-dev

COPY --from=builder /code/.venv /code/.venv

COPY main.py /code/main.py

COPY src /code/src

COPY alembic.ini /code/alembic.ini

COPY alembic /code/alembic

COPY scripts/integration-tests-entrypoint.sh /code/integration-tests-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "warning"]
