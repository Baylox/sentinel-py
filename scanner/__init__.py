from .core.config import ScanConfig
from .core.tcp import TCPScanner
from .exceptions import HostResolutionError, PortRangeError, PortScannerError
from .utils.validators import parse_port_range


def scan_ports(host: str, ports_range: str, timeout: float = 0.5) -> dict:
    """
    Convenience function to scan ports on a host.

    Args:
        host (str): Target IP address or domain name.
        ports_range (str): Port range in the format 'start-end' (e.g., '20-80').
        timeout (float): Timeout in seconds for each port connection attempt.

    Returns:
        dict: Dictionary containing:
            - 'open_ports': List of open port numbers
            - 'scan_results': List of dictionaries with detailed port information

    Raises:
        PortRangeError: If the port range is invalid.
        HostResolutionError: If the host cannot be resolved.
    """
    config = ScanConfig(
        host=host,
        ports=parse_port_range(ports_range),
        timeout=timeout,
    )
    return TCPScanner().scan(config)


__all__ = [
    "scan_ports",
    "ScanConfig",
    "TCPScanner",
    "PortScannerError",
    "PortRangeError",
    "HostResolutionError",
]
