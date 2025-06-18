from typing import Tuple

from ..exceptions import PortRangeError


def validate_port(port: int) -> bool:
    """
    Validates if a port number is within the valid range (1-65535).

    Args:
        port (int): Port number to validate.

    Returns:
        bool: True if port is valid, False otherwise.
    """
    return 1 <= port <= 65535


def parse_port_range(ports_range: str) -> Tuple[int, int]:
    """
    Parse and validate a port range string.

    Args:
        ports_range (str): Port range in the format 'start-end' (e.g., '20-80').

    Returns:
        Tuple[int, int]: Start and end ports.

    Raises:
        PortRangeError: If the port range is invalid.
    """
    try:
        start, end = map(int, ports_range.split("-"))
    except ValueError:
        raise PortRangeError("Invalid port range format. Use the format '20-80'.")

    if not (validate_port(start) and validate_port(end)):
        raise PortRangeError(
            f"Ports must be between 1 and 65535. Got range: {start}-{end}"
        )

    if start > end:
        raise PortRangeError(
            f"Start port ({start}) cannot be greater than end port ({end})"
        )

    return start, end
