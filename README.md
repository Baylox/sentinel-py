# SentinelPy

SentinelPy is a lightweight, modular vulnerability scanner built in Python. It performs local security checks such as port scanning, SSL certificate analysis, and HTTP header inspection. Designed for learning, auditing, and internal testing.

## Installation

### From PyPI (Coming Soon)

```bash
pip install sentinelpy
```

### From Source

1. Clone the repository:

   ```bash
   git clone https://github.com/Baylox/sentinel-py.git
   cd sentinel-py
   ```

2. Install in editable mode with dev dependencies:

   ```bash
   pip install -e ".[dev]"
   ```

   Or without dev tools:

   ```bash
   pip install -e .
   ```

## Usage

### Basic Scan

```bash
sentinelpy example.com 20-80
```

### Multi-Module Scan

```bash
sentinelpy example.com 20-443 --modules tcp http ssl
```

### SSL Certificate Check

```bash
sentinelpy google.com 443-443 --modules ssl
```

### Export Results

```bash
sentinelpy example.com 20-80 --json results.json
```

### Legacy Usage (Direct Python)

```bash
python main.py example.com 20-80
```

For all options:

```bash
sentinelpy --help
```

## Development

### Setup Development Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.\.venv\Scripts\Activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Install with dev dependencies
pip install -e ".[dev]"
```

### Code Quality

```bash
# Format code
black scanner/ tests/
isort scanner/ tests/

# Lint
flake8 scanner/ tests/

# Run tests
pytest

# With coverage
pytest --cov=scanner --cov-report=html
```

## Project Roadmap

The [roadmap](./docs/ROADMAP.md) outlines upcoming features, milestones, and future improvements.

---

## Disclaimer

This tool is provided for **educational and authorized security testing purposes only**.  
You are solely responsible for using it **ethically and legally**.  
Do **not** use it against systems that you do not own or do not have explicit permission to test.

Even though this project is under the MIT License, the author assumes **no responsibility** for any misuse or illegal application of the code.

<p align="center">
  <img src="https://img.shields.io/badge/Usage-Ethical%20Hacking%20Only-yellow?style=flat-square" />
</p>
