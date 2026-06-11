from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from .config import ScanConfig


class BaseScanner(ABC):
    """
    Abstract base class for all scanner implementations.

    This class defines the common interface that all scanners must implement,
    ensuring consistency across different scanning modules (TCP, HTTP, SSL, etc.).

    Attributes:
        timeout (float): Default timeout for scanner operations in seconds.
        rate_limiter (Optional[RateLimiter]): Rate limiter to control scan speed.
    """

    @classmethod
    def setup_parser(cls, parser) -> None:
        """
        Optional method to add scanner-specific arguments to the CLI parser.
        """
        pass

    @abstractmethod
    def scan(self, config: ScanConfig) -> Dict[str, Any]:
        """
        Perform a scan on the specified host.

        This is an abstract method that must be implemented by all subclasses.

        Args:
            config (ScanConfig): Configuration for the scan containing host, ports, etc.

        Returns:
            Dict[str, Any]: Scan results. The structure depends on the scanner type.

        Raises:
            Various exceptions depending on the scanner implementation
            (e.g., HostResolutionError, ConnectionError, etc.)
        """
        pass
