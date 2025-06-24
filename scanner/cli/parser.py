import argparse
import re
from typing import List, Optional, Tuple


class CLIValidationError(Exception):
    """Custom exception for CLI validation errors."""
    pass


def validate_port_range(ports: str) -> Tuple[int, int]:
    """
    Validate and parse port range in the format 'start-end'.

    Args:
        ports: Port range string (e.g., "20-80")

    Returns:
        A tuple of start and end ports.

    Raises:
        CLIValidationError: If the port range is invalid.
    """
    if not re.match(r"^\d+-\d+$", ports):
        raise CLIValidationError("Port range must be in format 'start-end' (e.g., '20-80')")

    start, end = map(int, ports.split("-"))
    if not (1 <= start <= 65535 and 1 <= end <= 65535):
        raise CLIValidationError("Ports must be between 1 and 65535")

    if start > end:
        raise CLIValidationError("Start port must be less than or equal to end port")

    return start, end


def validate_host(host: str) -> str:
    """
    Validate the target host.

    Args:
        host: IP address or domain name

    Returns:
        A validated host string.

    Raises:
        CLIValidationError: If the host format is invalid.
    """
    ip_pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
    if re.match(ip_pattern, host):
        octets = host.split(".")
        if not all(0 <= int(octet) <= 255 for octet in octets):
            raise CLIValidationError("Invalid IP address: octets must be between 0 and 255")
        return host

    domain_pattern = r"^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z]{2,})*$"
    if not re.match(domain_pattern, host):
        raise CLIValidationError("Invalid host: must be a valid IP address or domain name")

    return host


def validate_timeout(timeout: float) -> float:
    """
    Validate the timeout value.

    Args:
        timeout: Timeout in seconds

    Returns:
        The validated timeout.

    Raises:
        CLIValidationError: If the timeout is out of bounds.
    """
    if not 0.1 <= timeout <= 10.0:
        raise CLIValidationError("Timeout must be between 0.1 and 10.0 seconds")
    return timeout


def is_utility_only(args: argparse.Namespace, remaining: list) -> bool:
    """
    Check if only utility options were passed.

    Args:
        args: Parsed arguments
        remaining: Remaining unparsed arguments

    Returns:
        True if only utility options are requested.
    """
    return (args.clean_exports or args.list_exports) and not remaining


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse and validate CLI arguments.

    Args:
        argv: Simulated argument list (for testing). Defaults to sys.argv[1:].

    Returns:
        A namespace with validated arguments.

    Raises:
        CLIValidationError (wrapped as parser.error) on failure.
    """
    # Phase 1 — parse only utility flags first
    pre_parser = argparse.ArgumentParser(add_help=False)
    pre_parser.add_argument("--clean-exports", action="store_true")
    pre_parser.add_argument("--list-exports", action="store_true")
    pre_args, remaining_args = pre_parser.parse_known_args(argv)

    if is_utility_only(pre_args, remaining_args):
        return pre_args

    # Phase 2 — full argument parser
    parser = argparse.ArgumentParser(description="Modular vulnerability scanner")

    # Required arguments
    required = parser.add_argument_group("Required arguments")
    required.add_argument("host", help="Target host (e.g., IP or domain name)")
    required.add_argument("ports", help="Port range (e.g., 20-80)")

    # Module selection
    required.add_argument(
        "--modules",
        nargs="+",
        choices=["tcp", "http", "ssl"],
        default=["tcp"],
        help="Scan modules to enable (default: tcp)",
    )

    # Scan options
    scan_opts = parser.add_argument_group("Scan options")
    scan_opts.add_argument(
        "-t", "--timeout", type=float, default=0.5,
        help="Timeout per scan request (default: 0.5s)"
    )

    # Output options
    output_opts = parser.add_argument_group("Output options")
    output_opts.add_argument("--json", metavar="FILENAME", help="Export results to JSON file")
    output_opts.add_argument("--print-json", action="store_true", help="Print results in JSON format")

    # Logging options
    log_opts = parser.add_argument_group("Logging options")
    log_opts.add_argument("--logfile", metavar="FILENAME", help="Log to a custom file")
    log_opts.add_argument("--show-logs", action="store_true", help="Show logs after execution")
    log_opts.add_argument("--clear-logs", action="store_true", help="Clear logs before running")

    # Utility options
    utility_opts = parser.add_argument_group("Utility operations")
    utility_opts.add_argument("--clean-exports", action="store_true", help="Delete previous JSON exports")
    utility_opts.add_argument("--list-exports", action="store_true", help="List saved JSON exports")

    # Display options
    display_opts = parser.add_argument_group("Display options")
    display_opts.add_argument("--verbose", action="store_true", help="Show closed ports too")

    # Parse and validate
    args = parser.parse_args(remaining_args)

    try:
        args.ports = validate_port_range(args.ports)
        args.timeout = validate_timeout(args.timeout)
        args.host = validate_host(args.host)
    except CLIValidationError as e:
        parser.error(str(e))

    return args
