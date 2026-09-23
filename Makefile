all: run

install:
	uv sync

run: install
	HF_HOME=/tmp/$${USER}_hf_cache UV_CACHE_DIR=/tmp/$${USER}_uv_cache PYTHONPATH=. uv run python -m src

debug: install
	PYTHONPATH=. uv run python -m pdb -m src

clean:
	rm -rf __pycache__ src/__pycache__ .mypy_cache

fclean:
	$(clean)
	rm -rf .venv

lint:
	uv run flake8 src/
	uv run mypy src/ --warn-return-any --warn-unused-ignores

lint-strict:
	uv run flake8 src/
	uv run mypy src/ --strict

.PHONY: all install run debug clean lint lint-strict