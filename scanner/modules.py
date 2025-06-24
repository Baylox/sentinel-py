from scanner.core.tcp import TCPScanner
from scanner.core.http import HTTPScanner  
from typing import Dict

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

    return results

