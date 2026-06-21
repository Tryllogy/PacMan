install:
	uv sync

run: install
	uv run python3 -m src