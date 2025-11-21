import json
import logging
from typing import Any, Dict

from scanner.logging import log_with_context
from scanner.utils.exporter import export_to_json, export_to_csv


def display_results(results: Dict[str, Any]) -> None:
    logger = logging.getLogger("sentinelpy")
    log_with_context(
        logger, logging.DEBUG, "Rendering results to stdout", context="DISPLAY"
    )

    if not results:
        print("No results to display.")
        return

    print("\nScan Summary:")
    print("-" * 50)

    for module_name, module_data in results.items():
        print(f"[{module_name.upper()} Module]")

        open_ports = module_data.get("open_ports", [])
        scan_results = module_data.get("scan_results", [])

        print(
            f"Open ports: {', '.join(map(str, open_ports)) if open_ports else 'None'}"
        )
        print("Detailed Results:")

        for entry in scan_results:
            port = entry.get("port")
            status = entry.get("status", "unknown")
            service = entry.get("service", "N/A")
            error = entry.get("error", "")

            line = f"  - Port {port:<5} | Status: {status:<6} | Service: {service}"
            if error:
                line += f" | Error: {error}"
            print(line)

        print("-" * 50)

    log_with_context(
        logger, logging.INFO, "Results displayed successfully", context="DISPLAY"
    )


def handle_output(results: Dict[str, Any], args: Any) -> None:
    logger = logging.getLogger("sentinelpy")

    if args.json:
        log_with_context(
            logger, logging.INFO, f"Exporting results to {args.json}", context="EXPORT"
        )
        try:
            # Create parent directories if they don't exist
            from pathlib import Path
            Path(args.json).parent.mkdir(parents=True, exist_ok=True)
            
            with open(args.json, "w") as f:
                json.dump(results, f, indent=2)
            log_with_context(
                logger, logging.INFO, "Results exported successfully", context="EXPORT"
            )
        except (IOError, OSError) as e:
            log_with_context(
                logger, logging.ERROR, f"Export failed: {str(e)}", context="EXPORT"
            )
            raise

    if hasattr(args, "csv") and args.csv:
        log_with_context(
            logger, logging.INFO, f"Exporting results to {args.csv}", context="EXPORT"
        )
        try:
            export_to_csv(results, args.host, args.csv)
            log_with_context(
                logger, logging.INFO, "Results exported successfully", context="EXPORT"
            )
        except (IOError, OSError) as e:
            log_with_context(
                logger, logging.ERROR, f"Export failed: {str(e)}", context="EXPORT"
            )
            raise

    if args.print_json:
        log_with_context(
            logger, logging.DEBUG, "Printing results as JSON", context="EXPORT"
        )
        print(json.dumps(results, indent=2))
        log_with_context(
            logger, logging.INFO, "Results printed as JSON", context="EXPORT"
        )
