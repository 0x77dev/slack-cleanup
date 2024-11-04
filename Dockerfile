# syntax=docker/dockerfile:1.4
FROM python:3.11-slim as builder

LABEL org.opencontainers.image.title="Slack Cleanup"
LABEL org.opencontainers.image.description="A CLI tool for cleaning up Slack messages"
LABEL org.opencontainers.image.authors="Mykhailo Marynenko <mykhailo@0x77.dev>"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.source="https://github.com/0x77dev/slack-cleanup"

# Install build dependencies
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN --mount=type=cache,target=/root/.cache \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Set working directory
WORKDIR /app

# Copy files
COPY . ./

# Configure poetry and install dependencies
RUN --mount=type=cache,target=/root/.cache/pypoetry \
    --mount=type=cache,target=/root/.cache/pip \
    poetry config virtualenvs.in-project true && \
    poetry install --no-dev --no-interaction --no-ansi

# Build wheel
RUN poetry build --format wheel

# Runtime stage
FROM python:3.11-slim

LABEL org.opencontainers.image.title="Slack Cleanup"
LABEL org.opencontainers.image.description="A CLI tool for cleaning up Slack messages"
LABEL org.opencontainers.image.authors="Mykhailo Marynenko <mykhailo@0x77.dev>"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.source="https://github.com/0x77dev/slack-cleanup"

# Create non-root user
RUN useradd -m -U app && \
    mkdir -p /app && \
    chown app:app /app

WORKDIR /app

# Copy built wheel and virtual environment from builder
COPY --from=builder /app/dist/*.whl ./
COPY --from=builder /app/.venv ./.venv

# Install the wheel
RUN --mount=type=cache,target=/root/.cache/pip \
    ./.venv/bin/pip install *.whl && \
    rm *.whl

# Switch to non-root user
USER app

# Add virtual environment to path
ENV PATH="/app/.venv/bin:$PATH"

# Set entrypoint
ENTRYPOINT ["slack-cleanup"]