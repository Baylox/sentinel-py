SentinelPy is a lightweight, modular vulnerability scanner built in Python. It performs local security checks such as port scanning, SSL certificate analysis, and HTTP header inspection. Designed for learning, auditing, and internal testing.

```bash
.\.venv\Scripts\Activate
```

## Usage Examples

```bash
python main.py example.com 20-25
```

```bash
python main.py example.com 20-25 --print-json
```

### Automatic export 
```bash
python main.py localhost 70-80
```

```bash
python main.py localhost 22-80 --json test_output
```

```bash
python main.py localhost 22-80 --print-json
```

```bash
python main.py localhost 22-80 --json test_output --print-json
```

```bash
python main.py --clean-exports
```

```bash
python main.py --list-exports
```
### Tests and Logs
```bash
# Basic scan test
python main.py localhost 20-25
```
```bash
# Scan with custom log file
python main.py localhost 20-25 --logfile test.log
```

```bash
# Scan with log cleanup and log display
python main.py localhost 20-25 --clear-logs --show-logs
```

```bash
# Full scan test with all logging options
python main.py localhost 20-25 --logfile test.log --clear-logs --show-logs
```

## Flake8

Flake8 commands to check code quality and detect common errors:

```bash
# Full analysis with sorted results
flake8 scanner/ tests/ --format=default | sort
```

```bash
# Search for style errors (E) and failures (F) or other
flake8 scanner/ tests/ --select=F,E
```

```bash
# Search only for "Failure" errors (F) or other
flake8 scanner/ tests/ --select=F 
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
