class PortScannerError(Exception):
    """Base exception for all port scanner errors."""

    pass


class PortRangeError(PortScannerError):
    """Raised when there is an error with the port range specification."""

    pass


class HostResolutionError(PortScannerError):
    """Raised when the target host cannot be resolved."""

    pass
