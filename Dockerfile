FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
WORKDIR /app
COPY pyproject.toml LICENSE ./
COPY src ./src
RUN uv pip install --system --no-cache .

FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN useradd -m -u 1000 hornet
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY src ./src
COPY alembic.ini ./
COPY migrations ./migrations
ENV PYTHONPATH=/app/src
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app/logs && chown -R hornet:hornet /app/logs
USER hornet
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=3s --start-period=30s --retries=3 CMD curl -f http://localhost:8000/healthz || exit 1
CMD ["sh", "-c", "alembic upgrade head && uvicorn hornet.main:app --host 0.0.0.0 --port 8000"]
