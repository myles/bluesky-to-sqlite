.PHONY: setup
setup:
	uv sync --all-groups

.PHONY: test
test:
	uv run pytest --cov=bluesky_to_sqlite --cov-report=xml

.PHONY: lint
lint: ruff/check ruff/format ty

.PHONY: lint/fix
lint/fix: ruff/check/fix ruff/format/fix

.PHONY: ci
ci: lint test

.PHONY: ruff/check
ruff/check:
	uv run ruff check --statistics src/

.PHONY: ruff/check/fix
ruff/check/fix:
	uv run ruff check src/ --fix

.PHONY: ruff/format
ruff/format:
	uv run ruff format src/ --check

.PHONY: ruff/format/fix
ruff/format/fix:
	uv run ruff format src/

.PHONY: ty
ty:
	uv run ty check
