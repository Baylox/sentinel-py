import sys
import logging
from scanner import scan_ports, PortScannerError
from scanner.cli.parser import parse_args, CLIValidationError
from scanner.cli.display import display_results, handle_output
from scanner.cli.handlers import handle_utility_operations
from scanner.logging_advanced import setup_advanced_logger, log_with_context, SUCCESS
from scanner.logging_config import clear_logs, show_logs

def run_cli():
    """
    Entry point for the command-line interface.
    Coordinates argument parsing, scanning, displaying, and exporting.
    """
    # Initialize logger first to ensure it's available for error handling
    logger = None
    try:
        args = parse_args()
        
        # Clear logs if requested
        if hasattr(args, 'clear_logs') and args.clear_logs:
            log_with_context(logger, logging.INFO, "Clearing log files", context="CLI") if logger else None
            clear_logs()
        
        # Setup logger with custom logfile if specified
        logger = setup_advanced_logger(args.logfile if hasattr(args, 'logfile') else None)
        log_with_context(logger, logging.DEBUG, "CLI started with arguments: %s", args, context="CLI")

        # Handle utility operations first
        log_with_context(logger, logging.DEBUG, "Handling utility operations...", context="CLI")
        if handle_utility_operations(args):
            log_with_context(logger, logging.INFO, "Utility operation completed", context="CLI")
            return 0

        # Start scanning the target host and port range
        start_port, end_port = args.ports
        # Convert tuple of ports back to string format expected by scan_ports
        ports_range = f"{start_port}-{end_port}"
        log_with_context(logger, logging.INFO, "Scanning %s on ports %s...", args.host, ports_range, context="SCAN")
        results = scan_ports(args.host, ports_range, timeout=args.timeout)
        log_with_context(logger, logging.DEBUG, "Scan completed, processing results", context="SCAN")

        # Display formatted results
        display_results(results)

        # Output/export results based on user input
        handle_output(results, args)
        log_with_context(logger, SUCCESS, "Scan completed successfully", context="SCAN")

        # Show logs if requested
        if hasattr(args, 'show_logs') and args.show_logs:
            log_with_context(logger, logging.DEBUG, "Displaying log contents", context="CLI")
            print("\nLog contents:")
            print(show_logs(args.logfile if hasattr(args, 'logfile') else None))

    except CLIValidationError as e:
        # Handle validation errors
        if logger:
            log_with_context(logger, logging.ERROR, "Validation error: %s", str(e), context="CLI")
        else:
            print(f"Error: {e}", file=sys.stderr)
        return 1
    except PortScannerError as e:
        # Handle known errors (invalid host, range, etc.)
        if logger:
            log_with_context(logger, logging.ERROR, "Scanner error: %s", str(e), context="SCAN")
        else:
            print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        # Graceful exit on Ctrl+C
        if logger:
            log_with_context(logger, logging.WARNING, "Scan interrupted by user", context="CLI")
        else:
            print("\nScan interrupted by user.")
        return 1
    except Exception as e:
        # Handle unexpected errors
        if logger:
            log_with_context(logger, logging.ERROR, "Unexpected error: %s", str(e), context="CLI", exc_info=True)
        else:
            print(f"Unexpected error: {e}", file=sys.stderr)
        return 1

