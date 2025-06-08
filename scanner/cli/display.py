import logging
from typing import Dict, Any
from scanner.logging.logger import log_with_context
from scanner.utils.exporter import export_to_json
from scanner.utils.logging_tools import clear_logs, show_logs


def display_results(results: Dict[str, Any]) -> None:
    """
    Display scan results to the user with logging.

    Args:
        results: Dictionary containing scan results
    """
    logger = logging.getLogger("sentinelpy")
    log_with_context(logger, logging.DEBUG, "Rendering results to stdout", context="DISPLAY")

    open_ports = results.get("open_ports") or []
    scan_results = results.get("scan_results") or []

    # Compute column widths for clean alignment
    port_width = max([len(str(r["port"])) for r in scan_results] + [4])  # Minimum width for "Port"
    status_width = max([len(r["status"]) for r in scan_results] + [6])   # Minimum width for "Status"
    service_width = max([len(r.get("service") or "") for r in scan_results] + [7])  # Minimum "Service"

    print("\nScan Results:")
    print("-" * 50)

    # Display open ports
    open_ports_str = ", ".join(str(p) for p in open_ports) if open_ports else "None"
    print(f"Open ports: {open_ports_str}")

    # Display full scan table
    print("Scanned ports:")
    for r in scan_results:
        port = str(r["port"]).rjust(port_width)
        status = r["status"].ljust(status_width)
        service = r.get("service") or ""
        if service:
            print(f"  - {port}: {status}  ({service})")
        else:
            print(f"  - {port}: {status}")

    print("-" * 50)
    log_with_context(logger, logging.INFO, "Results displayed successfully", context="DISPLAY")

def handle_output(results: Dict[str, Any], args: Any) -> None:
    """
    Handle scan output export and display logic.

    Args:
        results: Dictionary containing scan results
        args: Parsed CLI arguments
    """
    logger = logging.getLogger("sentinelpy")

    if args.json:
        log_with_context(logger, logging.INFO, f"Exporting results to {args.json}", context="EXPORT")
        try:
            import json
            with open(args.json, 'w') as f:
                json.dump(results, f, indent=2)
            log_with_context(logger, logging.INFO, "Results exported successfully", context="EXPORT")
        except Exception as e:
            log_with_context(logger, logging.ERROR, f"Export failed: {str(e)}", context="EXPORT")
            raise

    if args.print_json:
        log_with_context(logger, logging.DEBUG, "Printing results as JSON", context="EXPORT")
        import json
        print(json.dumps(results, indent=2))
        log_with_context(logger, logging.INFO, "Results printed as JSON", context="EXPORT")

    else:
        # Default: export with an auto-generated name or default behavior
        export_to_json(results)
