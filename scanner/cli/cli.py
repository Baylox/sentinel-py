import sys
from scanner import scan_ports, PortScannerError
from scanner.cli.parser import parse_args, CLIValidationError
from scanner.cli.display import display_results, handle_output
from scanner.cli.handlers import handle_utility_operations

def run_cli():
    """
    Entry point for the command-line interface.
    Coordinates argument parsing, scanning, displaying, and exporting.
    """
    try:
        args = parse_args()

        # Handle utility operations first
        if handle_utility_operations(args):
            return 0

        # Start scanning the target host and port range
        start_port, end_port = args.ports
        # Convert tuple of ports back to string format expected by scan_ports
        ports_range = f"{start_port}-{end_port}"
        print(f"Scanning {args.host} on ports {ports_range}...")
        results = scan_ports(args.host, ports_range, timeout=args.timeout)

        # Display formatted results
        display_results(results)

        # Output/export results based on user input
        handle_output(results, args)

    except CLIValidationError as e:
        # Handle validation errors
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except PortScannerError as e:
        # Handle known errors (invalid host, range, etc.)
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        # Graceful exit on Ctrl+C
        print("\nScan interrupted by user.")
        return 1
    except Exception as e:
        # Handle unexpected errors
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1

