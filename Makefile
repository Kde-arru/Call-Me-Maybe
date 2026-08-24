all: run

install:
	uv sync

run: install
	PYTHONPATH=. uv run python -m src

debug: install
	PYTHONPATH=. uv run python -m pdb -m src

clean:
	rm -rf __pycache__ src/__pycache__ .mypy_cache .venv

lint:
	uv run flake8 src/
	uv run mypy src/ --warn-return-any --warn-unused-ignores

lint-strict:
	uv run flake8 src/
	uv run mypy src/ --strict

.PHONY: all install run debug clean lint lint-strict