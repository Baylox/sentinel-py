# SentinelPy Architecture

This document describes the architectural patterns and design decisions used in the SentinelPy project.

## Core Concepts (Services & DTOs)

While Python applications often avoid traditional Java/C# naming conventions like "Services" and "DTOs" (Data Transfer Objects) in their folder structures, **SentinelPy strictly adheres to these concepts under different names** to remain idiomatic to the Python ecosystem.

### 1. DTOs -> `models` & `config.py`

A DTO is an object used to encapsulate data and send it from one subsystem of an application to another without containing any business logic.

In SentinelPy, DTOs are located in:
- **`scanner.models`**: Contains the **Output DTOs** (`TCPScanResult`, `HTTPScanResult`, `SSLScanResult`). These models standardize the output of the scanners so that the CLI, display, and export modules can consume the data uniformly regardless of the underlying scanner type.
- **`scanner.core.config.ScanConfig`**: Acts as an **Input DTO**. It groups together all the parameters (host, ports, timeout, extra arguments) required to execute a scan. The CLI parser instantiates this object and passes it to the scanners, completely decoupling the argument parsing from the execution logic.

### 2. Services -> `core`

A Service contains the business logic of the application. It receives inputs (DTOs), performs an operation, and returns an output (DTOs).

In SentinelPy, Services are located in:
- **`scanner.core`**: The scanner implementations (`TCPScanner`, `HTTPScanner`, `SSLScanner`) are pure business services. They inherit from `BaseScanner` and their single responsibility is to execute a scan based on the `ScanConfig` provided and return the corresponding output model.
- **`scanner.modules`**: Acts as a **Service Manager** or Orchestrator. It reads the requested modules, queries the `ScannerRegistry`, and coordinates the execution of multiple scanner services.

## Plugin System (Registry Pattern)

SentinelPy uses a Registry Pattern (`ScannerRegistry`) to allow for dynamic discovery and instantiation of scanners.
This guarantees adherence to the **Open/Closed Principle (OCP)**: you can add new scanners (like a vulnerability scanner) simply by creating a new class decorated with `@ScannerRegistry.register("name")`, without ever needing to modify the CLI parser or the core orchestration logic.

## CLI & Presentation Layer

The `scanner.cli` package acts as the Controller/Presentation layer. It is strictly responsible for:
1. Parsing user input (`parser.py`).
2. Displaying results in a human-readable format (`display.py`).
3. Handling side-effects like file exports (`exporter.py`).

It does **not** contain any scanning or business logic.
