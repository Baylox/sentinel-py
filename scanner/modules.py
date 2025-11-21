from typing import Dict, Optional
import logging

from scanner.core.http import HTTPScanner
from scanner.core.ssl import SSLScanner
from scanner.core.tcp import TCPScanner
from scanner.utils.rate_limiter import RateLimiter

logger = logging.getLogger(__name__)


def create_rate_limiter(args) -> Optional[RateLimiter]:
    """Create a rate limiter based on CLI arguments.
    
    For safety, enforces minimal rate limiting (aggressive preset) for scans
    over 1000 ports even when 'none' is selected.
    
    Args:
        args: Parsed CLI arguments
    
    Returns:
        RateLimiter instance or None if rate limiting is disabled for small scans
    """
    # Custom delay overrides the preset
    if hasattr(args, 'delay') and args.delay is not None:
        return RateLimiter(delay=args.delay)
    
    # Use preset (may return None if preset='none')
    preset = getattr(args, 'preset', 'normal')
    rate_limiter = RateLimiter.from_preset(preset)
    
    # Safety check: enforce minimal rate limiting for large scans
    if rate_limiter is None:  # preset='none'
        start_port, end_port = args.ports
        port_count = end_port - start_port + 1
        
        if port_count > 1000:
            logger.warning(
                f"Large scan detected ({port_count} ports). "
                f"Enforcing minimal rate limiting (aggressive preset) for safety."
            )
            rate_limiter = RateLimiter.from_preset('aggressive')
    
    return rate_limiter


def run_selected_modules(args, logger) -> Dict[str, list]:
    results = {}

    start_port, end_port = args.ports
    port_range_str = f"{start_port}-{end_port}"
    
    # Create rate limiter based on CLI arguments
    rate_limiter = create_rate_limiter(args)

    if not hasattr(args, "modules") or not args.modules:
        tcp = TCPScanner(timeout=args.timeout, rate_limiter=rate_limiter)
        results["tcp"] = tcp.scan(args.host, port_range_str)
        return results

    if "tcp" in args.modules:
        tcp = TCPScanner(timeout=args.timeout, rate_limiter=rate_limiter)
        results["tcp"] = tcp.scan(args.host, port_range_str)

    if "http" in args.modules:
        http = HTTPScanner(timeout=args.timeout, rate_limiter=rate_limiter)
        results["http"] = http.scan(args.host, list(range(start_port, end_port + 1)))

    if "ssl" in args.modules:
        ssl_scanner = SSLScanner(timeout=args.timeout, verify=not args.no_verify, rate_limiter=rate_limiter)
        results["ssl"] = ssl_scanner.scan(args.host, getattr(args, "ssl_port", 443))

    return results
