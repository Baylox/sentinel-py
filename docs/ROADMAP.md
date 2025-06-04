# Project Roadmap – SentinelPy

## Phase 1: Basic TCP Scanner (Completed)
- Modular structure with `scan_ports()`
- Command-line interface (CLI) via `run_cli()` in `scanner/cli/cli.py`
- Automatic JSON export with timestamp
- Support for `--json` and `--print-json` flags
- Progress bar integration using `tqdm`
- Entry point defined in `main.py`

## Phase 2: CLI Enhancements and Maintenance
- Implement `--clean-exports` to remove previous JSON export files
- Implement `--list-exports` to display existing exports
- Add validation and error handling to CLI arguments
- Optional: support export of logs or structured logging

## Phase 3: HTTP and SSL Scanning
- HTTP scanner to retrieve headers (e.g., status, server type)
- SSL scanner to check certificate validity, expiration dates, common names, etc.
- Optional: support for subdomain scanning
- Modularize components into `http.py` and `ssl.py` within `scanner/core/`

## Phase 4: Testing and Code Quality
- Add unit tests using `pytest`
- Mock networking components (e.g., `socket`) for isolated tests
- Apply code formatting and linting using `black`, `flake8`, and `isort`
- Generate code coverage reports with `pytest-cov`

## Phase 5: Packaging and Distribution
- Create `pyproject.toml` or `setup.py` for packaging
- Add a CLI entry point (e.g., `sentinelpy scan ...`)
- Finalize and document usage in `README.md` with practical examples
