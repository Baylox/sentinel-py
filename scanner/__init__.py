from .core.tcp import TCPScanner
from .exceptions import HostResolutionError, PortRangeError, PortScannerError


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
    """
    scanner = TCPScanner(timeout=timeout)
    return scanner.scan(host, ports_range)


__all__ = [
    "scan_ports",
    "TCPScanner",
    "PortScannerError",
    "PortRangeError",
    "HostResolutionError",
]

