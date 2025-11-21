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

## Rate Limiting

SentinelPy includes built-in rate limiting to prevent target overload and reduce scan detectability. This is **essential for ethical scanning** and helps avoid unintentional denial-of-service.

### Presets

| Preset                | Delay             | Requests/sec | Use Case                                 |
| --------------------- | ----------------- | ------------ | ---------------------------------------- |
| `--preset stealth`    | ~1s (with jitter) | ~1 req/s     | Discrete scans, simulates human behavior |
| `--preset normal`     | 50ms              | ~20 req/s    | **Default**, balanced speed and stealth  |
| `--preset aggressive` | 10ms              | ~100 req/s   | Fast scans on internal networks          |
| `--preset none`       | No delay          | Unlimited    | Local testing only, **not recommended**  |

### Examples

```bash
# Default scan (normal preset: 50ms delay, ~20 req/s)
sentinelpy example.com 1-1000

# Stealth scan for external targets
sentinelpy example.com 1-1000 --preset stealth

# Fast scan for internal networks
sentinelpy 192.168.1.1 1-1000 --preset aggressive

# Custom delay (5 requests per second)
sentinelpy example.com 1-100 --delay 0.2

# Disable rate limiting (use responsibly)
sentinelpy localhost 1-1000 --preset none
```

> [!WARNING] > **Ethical Use**: Even with rate limiting disabled, you must only scan systems you own or have explicit authorization to test. Unauthorized scanning may be illegal.

> [!IMPORTANT] > **Safety Features**:
>
> - When using `--preset none`, a warning will be logged to remind you of the risks
> - For scans over 1000 ports with `--preset none`, the aggressive preset (10ms delay) is automatically enforced to prevent accidental DoS
> - These safety measures protect both you and your targets

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
