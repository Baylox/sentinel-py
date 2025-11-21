import socket
import ssl
from datetime import datetime, timezone
from typing import Any, Dict

from ..models.results import SSLScanResult
from .base import BaseScanner


class SSLScanner(BaseScanner):
    def __init__(self, timeout=5.0, verify=True, rate_limiter=None):
        super().__init__(timeout, rate_limiter)
        self.verify = verify

    def _parse_dt(self, s):
        """Parse SSL certificate date string into datetime object.
        
        Args:
            s: Date string from certificate (e.g., 'Jan  1 00:00:00 2024 GMT')
            
        Returns:
            datetime object or None if parsing fails
        """
        if not isinstance(s, str):
            return None
        for fix in (lambda x: x, lambda x: x.replace("  ", " ")):
            try:
                dt = datetime.strptime(fix(s), "%b %d %H:%M:%S %Y %Z").replace(
                    tzinfo=timezone.utc
                )
                return dt
            except ValueError as e:
                # Log the parsing failure for debugging
                import logging
                logger = logging.getLogger("sentinelpy")
                logger.debug(f"Failed to parse certificate date '{s}': {e}")
                continue
        return None

    def _flatten(self, name):
        out = {}
        for group in name:
            for k, v in group:
                out[k] = v
        return out

    def scan(self, host: str, port: int = 443) -> Dict[str, Any]:
        # Apply rate limiting if configured
        if self.rate_limiter:
            self.rate_limiter.wait()
        
        ctx = ssl.create_default_context()
        if not self.verify:
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

        try:
            with socket.create_connection((host, port), timeout=self.timeout) as sock:
                with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                    cert = ssock.getpeercert()

            if not cert:
                return SSLScanResult(
                    ok=False, error="No certificate presented"
                ).to_dict()

            subj = self._flatten(cert.get("subject", ()))
            issu = self._flatten(cert.get("issuer", ()))
            nb = self._parse_dt(cert.get("notBefore"))
            na = self._parse_dt(cert.get("notAfter"))
            days_left = (na - datetime.now(timezone.utc)).days if na else None

            return SSLScanResult(
                ok=True,
                issued_to=subj.get("commonName"),
                issued_by=issu.get("commonName"),
                valid_from=nb.isoformat() if nb else None,
                valid_until=na.isoformat() if na else None,
                days_left=days_left,
                expired=(days_left is not None and days_left < 0),
            ).to_dict()

        except ssl.SSLError as e:
            return SSLScanResult(ok=False, error=f"SSL error: {e}").to_dict()
        except OSError as e:
            return SSLScanResult(ok=False, error=f"Socket error: {e}").to_dict()
