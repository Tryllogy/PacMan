ARGS := ./src/config/config.json

.PHONY: install run debug clean lint lint-strict build

install:
	uv sync

run:
	uv run python3 pac-man.py $(ARGS)

debug:
	uv run python3 -m pdb pac-man.py $(ARGS)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

lint:
	uv run flake8 . --exclude=.venv
	uv run mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	uv run flake8 . --exclude=.venv
	uv run mypy . --strict

build:
	uv run pyinstaller --onedir --name pacman \
		--add-data "src/sprites:src/sprites" \
		--add-data "src/config:src/config" \
		pac-man.py