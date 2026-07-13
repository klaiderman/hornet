.PHONY: install run test test-integration lint up migrate seed

install:
	uv sync

run:
	uv run uvicorn hornet.main:app --reload --host 0.0.0.0 --port 8000

test:
	uv run pytest

test-integration:
	uv run pytest -m integration

lint:
	uv run ruff check .

up:
	docker compose up --build

migrate:
	uv run alembic upgrade head

seed:
	uv run python scripts/seed.py
