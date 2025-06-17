import argparse
import re
from typing import List, Optional, Tuple


class CLIValidationError(Exception):
    """Custom exception for CLI validation errors."""

    pass


def validate_port_range(ports: str) -> Tuple[int, int]:
    """
    Validate and parse port range.

    Args:
        ports: Port range string (e.g., "20-80")

    Returns:
        Tuple[int, int]: Start and end ports

    Raises:
        CLIValidationError: If port range is invalid
    """
    if not re.match(r"^\d+-\d+$", ports):
        raise CLIValidationError(
            "Port range must be in format 'start-end' (e.g., '20-80')"
        )

    start, end = map(int, ports.split("-"))

    if not (1 <= start <= 65535 and 1 <= end <= 65535):
        raise CLIValidationError("Ports must be between 1 and 65535")

    if start > end:
        raise CLIValidationError("Start port must be less than or equal to end port")

    return start, end


def validate_host(host: str) -> str:
    """
    Validate host address.

    Args:
        host: Host address (IP or domain name)

    Returns:
        str: Validated host address

    Raises:
        CLIValidationError: If host is invalid
    """
    # Basic IP validation
    ip_pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
    if re.match(ip_pattern, host):
        octets = host.split(".")
        if not all(0 <= int(octet) <= 255 for octet in octets):
            raise CLIValidationError(
                "Invalid IP address: octets must be between 0 and 255"
            )
        return host

    # Domain name validation (including localhost)
    domain_pattern = r"^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z]{2,})*$"
    if not re.match(domain_pattern, host):
        raise CLIValidationError(
            "Invalid host: must be a valid IP address or domain name"
        )

    return host


def validate_timeout(timeout: float) -> float:
    """
    Validate timeout value.

    Args:
        timeout: Timeout in seconds

    Returns:
        float: Validated timeout

    Raises:
        CLIValidationError: If timeout is invalid
    """
    if not 0.1 <= timeout <= 10.0:
        raise CLIValidationError("Timeout must be between 0.1 and 10.0 seconds")
    return timeout


def is_utility_only(args: argparse.Namespace, remaining: list) -> bool:
    """
    Check if only utility operations are requested.

    Args:
        args: Parsed arguments
        remaining: Remaining unparsed arguments

    Returns:
        bool: True if only utility operations are requested
    """
    return (args.clean_exports or args.list_exports) and not remaining


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command-line arguments.

    Args:
        argv: List of simulated arguments for testing. If None,
              the function reads sys.argv[1:].

    Returns:
        argparse.Namespace containing validated options.

    Raises:
        CLIValidationError via parser.error if validation fails.
    """
    # Phase 1 — minimal parser for utility flags
    pre_parser = argparse.ArgumentParser(add_help=False)
    pre_parser.add_argument("--clean-exports", action="store_true")
    pre_parser.add_argument("--list-exports", action="store_true")

    # parse_known_args accepts the provided list or sys.argv by default
    pre_args, remaining_args = pre_parser.parse_known_args(argv)

    if is_utility_only(pre_args, remaining_args):
        return pre_args  # nothing else to validate

    # Phase 2 — main parser
    parser = argparse.ArgumentParser(description="Network port scanner")

    # Required
    required = parser.add_argument_group("Required arguments")
    required.add_argument("host", help="Target host (IP address or domain name)")
    required.add_argument("ports", help="Port range (e.g., 20-80)")

    # Scan options
    scan_opts = parser.add_argument_group("Scan options")
    scan_opts.add_argument(
        "-t",
        "--timeout",
        type=float,
        default=0.5,
        help="Timeout in seconds for each port scan (default: 0.5)",
    )

    # Output options
    output_opts = parser.add_argument_group("Output options")
    output_opts.add_argument(
        "--json", metavar="FILENAME", help="Export scan results to a JSON file"
    )
    output_opts.add_argument(
        "--print-json",
        action="store_true",
        help="Print scan results as raw JSON to stdout",
    )

    # Logging options
    logging_opts = parser.add_argument_group("Logging options")
    logging_opts.add_argument(
        "--logfile", metavar="FILENAME", help="Write logs to custom log file"
    )
    logging_opts.add_argument(
        "--show-logs", action="store_true", help="Print logs to console after execution"
    )
    logging_opts.add_argument(
        "--clear-logs", action="store_true", help="Clear log file before starting"
    )

    # Utility options
    utility_opts = parser.add_argument_group("Utility operations")
    utility_opts.add_argument(
        "--clean-exports",
        action="store_true",
        help="Remove existing JSON exports before scanning",
    )
    utility_opts.add_argument(
        "--list-exports", action="store_true", help="List existing JSON exports"
    )

    # Display options
    display_opts = parser.add_argument_group("Display options")
    display_opts.add_argument(
        "--verbose",
        action="store_true",
        help="Show all ports scanned, including closed ones",
    )

    # Parse the remaining arguments
    args = parser.parse_args(remaining_args)

    # --- Custom validations ----------------------------------------
    # Validate arguments in order of importance
    try:
        # First validate port range as it's most likely to be wrong
        start_port, end_port = validate_port_range(args.ports)
        args.ports = (start_port, end_port)  # Store as tuple

        # Then validate timeout
        args.timeout = validate_timeout(args.timeout)

        # Finally validate host
        args.host = validate_host(args.host)

    except CLIValidationError as e:
        # Use parser.error to show proper usage
        parser.error(str(e))

    return args
