FROM debian:13-slim AS build

RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes python3 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml uv.lock ./

ENV UV_PYTHON_DOWNLOADS=never
RUN --mount=from=ghcr.io/astral-sh/uv:0.13,source=/uv,target=/usr/bin/uv \
    uv sync --locked --no-dev --no-cache --compile-bytecode --python /usr/bin/python3.13

FROM gcr.io/distroless/python3-debian13

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY --from=build /app/.venv /app/.venv
COPY . /app

# discord.py only shuts down cleanly on SIGINT
STOPSIGNAL SIGINT

ENTRYPOINT ["/app/.venv/bin/python3", "run.py"]
