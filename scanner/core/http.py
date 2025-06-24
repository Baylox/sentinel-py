import requests
from typing import List, Dict, Any
from tqdm import tqdm

class HTTPScanner:
    def __init__(self, timeout: float = 3.0):
        """Initialize the HTTP scanner with a timeout value."""
        self.timeout = timeout

    def scan(self, host: str, ports: List[int]) -> Dict[str, Any]:
        """
        Scan a list of ports on the specified host for HTTP services.
        
        Args:
            host: The target hostname or IP.
            ports: A list of ports to scan.
        
        Returns:
            A dictionary containing open ports and detailed scan results.
        """
        open_ports = []
        results = []

        for port in tqdm(ports, desc="Scanning HTTP ports", unit="port"):
            url = f"http://{host}:{port}/"
            try:
                response = requests.get(url, timeout=self.timeout)
                is_open = response.ok

                if is_open:
                    open_ports.append(port)

                results.append({
                    "port": port,
                    "status": "open" if is_open else "closed",
                    "status_code": response.status_code,
                    "server": response.headers.get("Server", "Unknown"),
                    "content_type": response.headers.get("Content-Type", "Unknown"),
                    "url": url
                })
            except Exception as e:
                results.append({
                    "port": port,
                    "status": "closed",
                    "error": str(e),
                    "url": url
                })

        return {
            "open_ports": open_ports,
            "scan_results": results
        }

