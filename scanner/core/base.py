from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseScanner(ABC):
    """
    Abstract base class for all scanner implementations.

    This class defines the common interface that all scanners must implement,
    ensuring consistency across different scanning modules (TCP, HTTP, SSL, etc.).

    Attributes:
        timeout (float): Default timeout for scanner operations in seconds.
        rate_limiter (Optional[RateLimiter]): Rate limiter to control scan speed.
    """

    def __init__(self, timeout: float = 0.5, rate_limiter: Optional[Any] = None):
        """
        Initialize the base scanner.

        Args:
            timeout (float): Default timeout for scanner operations in seconds.
                           Different scanners may use different default values.
            rate_limiter (Optional[RateLimiter]): Rate limiter instance to control
                           request frequency. If None, no rate limiting is applied.
        """
        self.timeout = timeout
        self.rate_limiter = rate_limiter

    @abstractmethod
    def scan(self, host: str, *args, **kwargs) -> Dict[str, Any]:
        """
        Perform a scan on the specified host.

        This is an abstract method that must be implemented by all subclasses.
        The exact signature and behavior will vary depending on the scanner type:

        - TCPScanner: scan(host, ports_range: str) -> Dict[str, list]
        - HTTPScanner: scan(host, ports: List[int]) -> Dict[str, Any]
        - SSLScanner: scan(host, port: int = 443) -> Dict[str, Any]

        Args:
            host (str): Target host (IP address or domain name).
            *args: Additional positional arguments specific to the scanner.
            **kwargs: Additional keyword arguments specific to the scanner.

        Returns:
            Dict[str, Any]: Scan results. The structure depends on the scanner type
                          but typically includes information about discovered services,
                          open ports, or security findings.

        Raises:
            Various exceptions depending on the scanner implementation
            (e.g., HostResolutionError, ConnectionError, etc.)
        """
        pass
