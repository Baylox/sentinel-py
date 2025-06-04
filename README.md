SentinelPy is a lightweight, modular vulnerability scanner built in Python. It performs local security checks such as port scanning, SSL certificate analysis, and HTTP header inspection. Designed for learning, auditing, and internal testing.

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
