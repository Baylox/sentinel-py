# SentinelPy Makefile
# ------------------------------------------------------------
# Usage: make <target>
# Run `make help` to list available targets
# ------------------------------------------------------------

# phony targets
.PHONY: help test lint format check coverage clean

PY = .venv/Scripts/python.exe  # Change to `python` if you always activate venv

help:       ## Show this help.
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) \
	    | awk 'BEGIN{FS=":.*?## "}; {printf "\033[36m%-12s\033[0m %s\n", $$1, $$2}'

test:       ## Run the unit-test suite
	$(PY) -m pytest

lint:       ## flake8 on source and tests
	$(PY) -m flake8 scanner tests

format:     ## Apply isort & black
	$(PY) -m isort .
	$(PY) -m black .

check:      ## Dry-run style & lint checks
	$(PY) -m isort . --check-only
	$(PY) -m black . --check
	$(PY) -m flake8 scanner tests

coverage:   ## Run tests with coverage report (HTML + terminal)
	$(PY) -m pytest --cov=scanner --cov-report=term-missing --cov-report=html

clean:      ## Remove caches & coverage artifacts (cross-platform)
	@if exist .pytest_cache rmdir /s /q .pytest_cache || true
	@if exist htmlcov       rmdir /s /q htmlcov       || true
	@if exist .coverage     del          .coverage    || true
