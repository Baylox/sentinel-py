import socket
from typing import Dict

from tqdm import tqdm

from ..exceptions import HostResolutionError
from ..models.ports import PortResult, PortScanResults
from ..utils.validators import parse_port_range


class PortScanner:
    """Main port scanner implementation."""

    def __init__(self, timeout: float = 0.5):
        """
        Initialize the port scanner.

        Args:
            timeout (float): Default timeout for port connections in seconds.
        """
        self.timeout = timeout

    def _check_host_resolution(self, host: str) -> None:
        """
        Verify that the host can be resolved.

        Args:
            host (str): Host to check.

        Raises:
            HostResolutionError: If the host cannot be resolved.
        """
        try:
            socket.gethostbyname(host)
        except socket.gaierror as e:
            raise HostResolutionError(f"Could not resolve hostname '{host}': {str(e)}")

    def _scan_single_port(self, host: str, port: int) -> PortResult:
        """
        Scan a single port on the target host.

        Args:
            host (str): Target host.
            port (int): Port to scan.

        Returns:
            PortResult: Result of the port scan.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                result = sock.connect_ex((host, port))

                status = "open" if result == 0 else "closed"
                service = ""

                if status == "open":
                    try:
                        service = socket.getservbyport(port)
                    except (OSError, socket.error):
                        service = "unknown"

                return PortResult(
                    port=port,
                    status=status,
                    service=service if status == "open" else "",
                )

        except socket.error as e:
            return PortResult(port=port, status="error", error=str(e))

    def scan(self, host: str, ports_range: str) -> Dict[str, list]:
        """
        Scan the specified TCP port range on a given host.

        Args:
            host (str): Target IP address or domain name.
            ports_range (str): Port range in the format 'start-end' (e.g., '20-80').

        Returns:
            dict: Dictionary containing scan results:
                - 'open_ports': List of open port numbers
                - 'scan_results': List of dictionaries with detailed port information

        Raises:
            HostResolutionError: If the host cannot be resolved
            PortRangeError: If the port range is invalid
        """
        # Verify host can be resolved
        self._check_host_resolution(host)

        # Parse and validate port range
        start, end = parse_port_range(ports_range)

        # Initialize results container
        results = PortScanResults()

        # Scan each port in range (using tqdm for progress bar)
        for port in tqdm(range(start, end + 1), desc=f"Scanning {host}"):
            result = self._scan_single_port(host, port)
            results.add_result(result)

        return results.to_dict()
