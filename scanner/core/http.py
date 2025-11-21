from typing import Any, Dict, List

import requests
from tqdm import tqdm

from ..models.results import HTTPScanResult
from .base import BaseScanner


class HTTPScanner(BaseScanner):
    def __init__(self, timeout: float = 3.0, rate_limiter=None):
        # Set the timeout for HTTP requests and pass rate_limiter to base
        super().__init__(timeout, rate_limiter)

    def _identify_web_server(self, server_header: str) -> str:
        """
        Identify common web servers from the 'Server' HTTP header.
        Falls back to a capitalized version of the raw server string if not matched.
        """
        if not server_header:
            return "Unknown"

        header = server_header.lower()

        if "apache" in header:
            return "Apache"
        elif "nginx" in header:
            return "Nginx"
        elif "iis" in header or "microsoft" in header:
            return "Microsoft IIS"
        elif "lighttpd" in header:
            return "Lighttpd"
        elif "gunicorn" in header:
            return "Gunicorn"
        elif "caddy" in header:
            return "Caddy"
        else:
            # Fallback: take the first part of the header (e.g., "Apache/2.4.41") => "Apache"
            return server_header.split("/")[0].capitalize()

    def scan(self, host: str, ports: List[int]) -> Dict[str, Any]:
        """
        Scan a list of ports on a host using HTTP requests to detect web services.

        Args:
            host: Target host (e.g., "localhost").
            ports: List of TCP ports to scan.

        Returns:
            Dict with open ports and detailed scan results per port.
        """
        open_ports = []
        results = []

        for port in tqdm(ports, desc="Scanning HTTP ports", unit="port"):
            # Apply rate limiting if configured
            if self.rate_limiter:
                self.rate_limiter.wait()
            
            url = f"http://{host}:{port}/"

            try:
                # Send GET request (disable SSL verification for scanning purposes)
                resp = requests.get(url, timeout=self.timeout, verify=False)
                server_header = resp.headers.get("Server", "Unknown")
                server_type = self._identify_web_server(server_header)

                if resp.ok:
                    open_ports.append(port)

                # Collect scan result for current port
                results.append(
                    {
                        "port": port,
                        "status": "open" if resp.ok else "closed",
                        "status_code": resp.status_code,
                        "server": server_type,
                        "content_type": resp.headers.get("Content-Type", "Unknown"),
                        "url": url,
                    }
                )

            except requests.RequestException as e:
                # If error occurs (timeout, connection refused, etc.)
                results.append(
                    {
                        "port": port,
                        "status": "closed",
                        "server": "N/A",
                        "error": str(e).split(" (")[
                            0
                        ],  # Only show the root error message
                        "url": url,
                    }
                )

        # Create HTTPScanResult
        http_result = HTTPScanResult(open_ports=open_ports, scan_results=results)

        return http_result.to_dict()
