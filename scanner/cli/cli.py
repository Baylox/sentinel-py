import sys
import argparse
import logging
from scanner import scan_ports, PortScannerError
from scanner.cli.parser import parse_args, CLIValidationError
from scanner.cli.display import display_results, handle_output
from scanner.cli.handlers import handle_utility_operations
from scanner.logger import setup_logger, log_with_context, SUCCESS, clear_logs, show_logs

def run_cli():
    """
    Entry point for the command-line interface.
    Coordinates argument parsing, scanning, displaying, and exporting.
    """

    # ────── PRE-PARSE FLAGS ──────
    pre_parser = argparse.ArgumentParser(add_help=False)
    pre_parser.add_argument("--clear-logs", action="store_true")
    args, _ = pre_parser.parse_known_args()

    if args.clear_logs:
        clear_logs()
        print("[✔] Logs supprimés.")
        return 0

    # ────── MAIN PARSING & LOGGING ──────
    logger = None
    try:
        args = parse_args()
        logger = setup_logger(args.logfile if hasattr(args, 'logfile') else None)
        log_with_context(logger, logging.DEBUG, "CLI started with arguments: %s", args, context="CLI")

        # ────── HANDLE UTILITY FLAGS ──────
        if handle_utility_operations(args):
            log_with_context(logger, logging.INFO, "Utility operation completed", context="CLI")
            return 0

        # ────── PORT SCAN EXECUTION ──────
        start_port, end_port = args.ports
        ports_range = f"{start_port}-{end_port}"
        log_with_context(logger, logging.INFO, "Scanning %s on ports %s...", args.host, ports_range, context="SCAN")

        results = scan_ports(args.host, ports_range, timeout=args.timeout)
        log_with_context(logger, logging.DEBUG, "Scan completed, processing results", context="SCAN")

        # ────── RESULTS & EXPORTS ──────
        display_results(results)
        handle_output(results, args)
        log_with_context(logger, SUCCESS, "Scan completed successfully", context="SCAN")

        if getattr(args, "show_logs", False):
            print("\nLog contents:")
            print(show_logs(args.logfile if hasattr(args, 'logfile') else None))

    # ────── EXCEPTION HANDLING ──────
    except CLIValidationError as e:
        print(f"[!] Invalid argument: {e}", file=sys.stderr)
        if logger:
            log_with_context(logger, logging.ERROR, "Validation error: %s", str(e), context="CLI")
        return 1

    except PortScannerError as e:
        print(f"[!] Scan error: {e}", file=sys.stderr)
        if logger:
            log_with_context(logger, logging.ERROR, "Scanner error: %s", str(e), context="SCAN")
        return 1

    except KeyboardInterrupt:
        print("\n[!] Scan interrompu.")
        if logger:
            log_with_context(logger, logging.WARNING, "Scan interrupted by user", context="CLI")
        return 1

    except Exception as e:
        print(f"[!] Unexpected error: {e}", file=sys.stderr)
        if logger:
            log_with_context(logger, logging.ERROR, "Unexpected error: %s", str(e), context="CLI", exc_info=True)
        return 1


