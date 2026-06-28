# SentinelPy Makefile
# ------------------------------------------------------------
# Usage: make <target>
# Run `make help` to list available targets
# ------------------------------------------------------------

# phony targets
.PHONY: help test lint typecheck format check coverage security clean

# Portable interpreter: defaults to `python`, override with `make PY=...`
# (e.g. `make PY=.venv/Scripts/python.exe` on Windows, or `make PY=python3`).
PY ?= python

help:       ## Show this help.
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) \
	    | awk 'BEGIN{FS=":.*?## "}; {printf "\033[36m%-12s\033[0m %s\n", $$1, $$2}'

test:       ## Run the unit-test suite
	$(PY) -m pytest

lint:       ## flake8 on source and tests
	$(PY) -m flake8 scanner tests

typecheck:  ## Static type-check with mypy
	$(PY) -m mypy scanner

security:   ## Static security scan (bandit) & dependency audit (pip-audit)
	$(PY) -m bandit -r scanner
	$(PY) -m pip_audit

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
