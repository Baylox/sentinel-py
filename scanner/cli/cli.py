import sys
from scanner import scan_ports, PortScannerError
from scanner.cli.parser import parse_args, CLIValidationError
from scanner.cli.display import display_results, handle_output
from scanner.cli.handlers import handle_utility_operations
from scanner.logging_config import setup_logger, clear_logs, show_logs

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
            clear_logs()
        
        # Setup logger with custom logfile if specified
        logger = setup_logger(args.logfile if hasattr(args, 'logfile') else None)
        logger.debug("CLI started with arguments: %s", args)

        # Handle utility operations first
        if handle_utility_operations(args):
            return 0

        # Start scanning the target host and port range
        start_port, end_port = args.ports
        # Convert tuple of ports back to string format expected by scan_ports
        ports_range = f"{start_port}-{end_port}"
        logger.info("Scanning %s on ports %s...", args.host, ports_range)
        results = scan_ports(args.host, ports_range, timeout=args.timeout)

        # Display formatted results
        display_results(results)

        # Output/export results based on user input
        handle_output(results, args)
        logger.info("Scan completed successfully")

        # Show logs if requested
        if hasattr(args, 'show_logs') and args.show_logs:
            print("\nLog contents:")
            print(show_logs(args.logfile if hasattr(args, 'logfile') else None))

    except CLIValidationError as e:
        # Handle validation errors
        if logger:
            logger.error("Validation error: %s", str(e))
        else:
            print(f"Error: {e}", file=sys.stderr)
        return 1
    except PortScannerError as e:
        # Handle known errors (invalid host, range, etc.)
        if logger:
            logger.error("Scanner error: %s", str(e))
        else:
            print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        # Graceful exit on Ctrl+C
        if logger:
            logger.warning("Scan interrupted by user")
        else:
            print("\nScan interrupted by user.")
        return 1
    except Exception as e:
        # Handle unexpected errors
        if logger:
            logger.error("Unexpected error: %s", str(e), exc_info=True)
        else:
            print(f"Unexpected error: {e}", file=sys.stderr)
        return 1

