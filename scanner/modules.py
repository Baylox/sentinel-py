from typing import Dict

from scanner.core.http import HTTPScanner
from scanner.core.ssl import SSLScanner
from scanner.core.tcp import TCPScanner


def run_selected_modules(args, logger) -> Dict[str, list]:
    results = {}

    start_port, end_port = args.ports
    port_range_str = f"{start_port}-{end_port}"

    if not hasattr(args, "modules") or not args.modules:
        tcp = TCPScanner(timeout=args.timeout)
        results["tcp"] = tcp.scan(args.host, port_range_str)
        return results

    if "tcp" in args.modules:
        tcp = TCPScanner(timeout=args.timeout)
        results["tcp"] = tcp.scan(args.host, port_range_str)

    if "http" in args.modules:
        http = HTTPScanner(timeout=args.timeout)
        results["http"] = http.scan(args.host, list(range(start_port, end_port + 1)))

    if "ssl" in args.modules:
        ssl_scanner = SSLScanner(timeout=args.timeout, verify=not args.no_verify)
        results["ssl"] = ssl_scanner.scan(args.host, getattr(args, "ssl_port", 443))

    return results
