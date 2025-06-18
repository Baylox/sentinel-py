from dataclasses import dataclass
from typing import List


@dataclass
class PortResult:
    """Represents the result of scanning a single port."""

    port: int
    status: str
    service: str = ""
    error: str = ""


class PortScanResults:
    """Container for all scan results."""

    def __init__(self):
        self.open_ports: List[int] = []
        self.scan_results: List[PortResult] = []

    def to_dict(self) -> dict:
        """Convert the results to a dictionary format."""
        return {
            "open_ports": self.open_ports,
            "scan_results": [vars(result) for result in self.scan_results],
        }

    def add_result(self, result: PortResult) -> None:
        """Add a new port scan result."""
        self.scan_results.append(result)
        if result.status == "open":
            self.open_ports.append(result.port)
