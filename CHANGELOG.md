# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-07-28

First public release. SentinelPy is a modular network reconnaissance tool: it
probes a host across a range of ports and reports what is listening, what web
server answers, and whether the TLS certificate is still valid. It performs no
exploitation and maintains no CVE database.

### Added

- **Scan modules.** Three interchangeable modules selected with `--modules` and
  combinable in a single run: `tcp` opens connections across the port range and
  names the service behind each open port from the system service table; `http`
  sends a GET request to every port and reports status code, server software and
  content type, recognising Apache, Nginx, Microsoft IIS, Lighttpd, Gunicorn and
  Caddy; `ssl` performs a TLS handshake on a single port and reports the
  certificate's issuer, subject, validity window and remaining days.
- **Scanner registry.** Scanners register themselves with
  `@ScannerRegistry.register("name")`; the CLI discovers them and their name
  becomes a valid `--modules` value automatically, so adding a module requires no
  change to the command-line layer.
- **Concurrent TCP scanning.** Ports are probed through a thread pool so that
  per-port timeouts overlap instead of accumulating, which matters most on
  filtered hosts. The worker count is configurable with `--workers` (1 to 1000,
  default 100) and is capped at the number of ports in range. Results are
  reassembled in ascending port order, so output is deterministic regardless of
  completion order.
- **Rate limiting.** Every request passes through a rate limiter, with the
  presets `stealth` (~1 req/s, randomised between 0.5x and 2x), `normal` (~20
  req/s, the default), `aggressive` (~100 req/s) and `none`. A fixed delay can be
  set directly with `--delay`. Two safeguards apply to `none`: it writes a
  warning to the log, and beyond 1000 ports the `aggressive` pacing is reinstated
  automatically so an unthrottled sweep of a large range cannot be launched by
  accident. Dispatch is paced on the submitting thread, which keeps the global
  rate bounded even while connections overlap.
- **Input validation.** Arguments are checked before any packet leaves the
  machine: ports must fall between 1 and 65535 with start not exceeding end, the
  timeout between 0.1 and 10.0 seconds, the worker count between 1 and 1000, and
  the host must be a syntactically valid IP address or domain name. For the `tcp`
  module the host is resolved first, so an unresolvable name fails immediately
  rather than after a full sweep of timeouts. Failures raise `PortScannerError`
  or its subclasses `PortRangeError` and `HostResolutionError`.
- **Path confinement.** Export and log filenames are confined to `exports/` and
  `logs/` respectively; a filename that attempts path traversal is rejected
  before anything is written.
- **Exports.** Results are written as JSON (`--json`), as CSV flattened across
  every module (`--csv`), or printed to stdout (`--print-json`). The `exports/`
  directory is managed with `--list-exports` and `--clean-exports`, which run
  standalone without a host or port range.
- **Logging.** Runs are logged to `logs/`, with `--logfile` to choose the file,
  `--show-logs` to print it afterwards and `--clear-logs` to empty the directory
  beforehand.
- **Python API.** The package is usable as a library: `scan_ports()` covers the
  common TCP case, while a `ScanConfig` passed to a scanner gives access to every
  option the CLI exposes.
- **Packaging.** Installable with `pip install -e .`, exposing a `sentinelpy`
  console entry point. Python 3.8 through 3.13 are supported. `main.py` remains an
  equivalent entry point for use without installation.
- **Continuous integration.** Every push and pull request runs the test suite
  across all six supported Python versions, plus separate lint, type-check and
  security jobs. The suite covers 79 tests with networking mocked for isolation.
- **Tooling.** `pre-commit` hooks run isort, black and flake8 on each commit, and
  a makefile wraps the usual tasks (`test`, `lint`, `typecheck`, `security`,
  `format`, `check`, `coverage`, `clean`).
- **Documentation.** A README covering every option, `docs/ARCHITECTURE.md` on
  the internal structure, `docs/ROADMAP.md` on project phases, and a runnable
  example under `examples/`.

[Unreleased]: https://github.com/Baylox/sentinel-py/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Baylox/sentinel-py/releases/tag/v0.1.0
