import sys
import argparse
import logging
from scanner import scan_ports, PortScannerError
from scanner.cli.parser import parse_args, CLIValidationError
from scanner.cli.display import display_results, handle_output
from scanner.cli.handlers import handle_utility_operations
from scanner.logger import (
    setup_logger,
    log_with_context,
    SUCCESS,
    clear_logs,
    show_logs,
)


def run_cli():
    """
    Entry point for the command-line interface.
    """
    if handle_clear_logs_flag():
        return 0

    logger = None
    try:
        args = parse_args()
        logger = setup_logger(args.logfile if hasattr(args, 'logfile') else None)
        log_with_context(logger, logging.DEBUG, "CLI started with arguments: %s", args, context="CLI")

        if handle_utility_ops(args, logger):
            return 0

        results = perform_scan(args, logger)
        handle_output_and_display(results, args, logger)

        return 0
    except Exception as e:
        return handle_cli_error(e, logger)


# ─────────────────────────────────────────────
# Utility Functions (Logic Decoupling)
# ─────────────────────────────────────────────

def handle_clear_logs_flag():
    """
    Check if --clear-logs was passed, and handle it before parsing other args.
    """
    pre_parser = argparse.ArgumentParser(add_help=False)
    pre_parser.add_argument("--clear-logs", action="store_true")
    args, _ = pre_parser.parse_known_args()

    if args.clear_logs:
        clear_logs()
        print("[✔] Logs deleted.")
        return True
    return False


def handle_utility_ops(args, logger):
    """
    Execute utility options like --list-exports or --show-logs early.
    """
    log_with_context(logger, logging.DEBUG, "Handling utility operations...", context="CLI")
    if handle_utility_operations(args):
        log_with_context(logger, logging.INFO, "Utility operation completed", context="CLI")
        return True
    return False


def perform_scan(args, logger):
    """
    Run the actual port scan.
    """
    start_port, end_port = args.ports
    ports_range = f"{start_port}-{end_port}"

    log_with_context(logger, logging.INFO, "Scanning %s on ports %s...", args.host, ports_range, context="SCAN")
    results = scan_ports(args.host, ports_range, timeout=args.timeout)
    log_with_context(logger, logging.DEBUG, "Scan completed", context="SCAN")

    return results


def handle_output_and_display(results, args, logger):
    """
    Show results and handle JSON export or log display.
    """
    display_results(results)
    handle_output(results, args)
    log_with_context(logger, SUCCESS, "Scan completed successfully", context="SCAN")

    if getattr(args, "show_logs", False):
        print("\nLog contents:")
        print(show_logs(args.logfile if hasattr(args, 'logfile') else None))


def handle_cli_error(e, logger):
    error_map = [
        (CLIValidationError, "Invalid argument", "CLI"),
        (PortScannerError, "Scanner error", "SCAN"),
        (KeyboardInterrupt, "Scan interrupted", "CLI"),
    ]

    for exc_type, msg, context in error_map:
        if isinstance(e, exc_type):
            print(f"[!] {msg}: {e}", file=sys.stderr)
            if logger:
                log_with_context(logger,
                                logging.WARNING if exc_type is KeyboardInterrupt else logging.ERROR,
                                f"{msg}: %s", str(e), context=context)
            return 1

    # Unexpected error fallback
    print(f"[!] Unexpected error: {e}", file=sys.stderr)
    if logger:
        log_with_context(logger, logging.ERROR, "Unexpected error: %s", str(e), context="CLI", exc_info=True)

    return 1




