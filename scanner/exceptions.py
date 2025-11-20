class PortScannerError(Exception):
    """Base exception for all port scanner errors."""

    pass


class PortRangeError(PortScannerError):
    """Raised when there is an error with the port range specification."""

    pass


class HostResolutionError(PortScannerError):
    """Raised when the target host cannot be resolved."""

    pass


class SSLScannerError(PortScannerError):
    """Base exception for SSL/TLS scanner errors."""

    pass


class CertificateNotFoundError(SSLScannerError):
    """Raised when no certificate is presented by the server."""

    pass


class SSLConnectionError(SSLScannerError):
    """Raised when SSL/TLS connection or handshake fails."""

    pass


class SSLValidationError(SSLScannerError):
    """Raised when SSL/TLS certificate validation fails."""

    pass

