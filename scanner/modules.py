from scanner.core.tcp import TCPScanner
from scanner.core.http import HTTPScanner  
from typing import Dict

def run_selected_modules(args, logger) -> Dict[str, list]:
    """
    Dynamically run scanning modules based on CLI arguments.

    Args:
        args: Parsed CLI arguments.
        logger: Logger instance.

    Returns:
        dict: Dictionary of results per module.
    """
    results = {}

    # Convert tuple to string "start-end"
    port_range_str = f"{args.ports[0]}-{args.ports[1]}"

    if not hasattr(args, "modules") or not args.modules:
        # Default behavior if no specific module selected
        tcp = TCPScanner(timeout=args.timeout)
        results["tcp"] = tcp.scan(args.host, port_range_str)
        return results

    if "tcp" in args.modules:
        tcp = TCPScanner(timeout=args.timeout)
        results["tcp"] = tcp.scan(args.host, port_range_str)

    if "http" in args.modules:
        http = HTTPScanner(timeout=args.timeout)
        results["http"] = http.scan(args.host)  # tu peux rajouter un port ou un chemin selon ton besoin

    return results
