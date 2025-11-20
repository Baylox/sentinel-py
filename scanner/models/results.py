from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TCPScanResult:
    """
    Result from a TCP port scan.

    Contains list of open ports and detailed scan results for each port.
    """

    open_ports: List[int] = field(default_factory=list)
    scan_results: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format for JSON serialization."""
        return asdict(self)


@dataclass
class HTTPScanResult:
    """
    Result from an HTTP scan.

    Contains HTTP-specific information such as server types and status codes.
    """

    open_ports: List[int] = field(default_factory=list)
    scan_results: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format for JSON serialization."""
        return asdict(self)


@dataclass
class SSLScanResult:
    """
    Result from an SSL/TLS certificate scan.

    Contains certificate information and validation status.
    """

    ok: bool = False
    issued_to: Optional[str] = None
    issued_by: Optional[str] = None
    valid_from: Optional[str] = None
    valid_until: Optional[str] = None
    days_left: Optional[int] = None
    expired: bool = False
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format for JSON serialization."""
        return asdict(self)
