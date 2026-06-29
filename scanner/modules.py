import logging
from typing import Dict, Optional

# Import scanners to trigger their registration with the ScannerRegistry.
import scanner.core.http  # noqa: F401
import scanner.core.ssl  # noqa: F401
import scanner.core.tcp  # noqa: F401
from scanner.core.config import ScanConfig
from scanner.core.registry import ScannerRegistry
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
    if hasattr(args, "delay") and args.delay is not None:
        return RateLimiter(delay=args.delay)

    # Use preset (may return None if preset='none')
    preset = getattr(args, "preset", "normal")
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
            rate_limiter = RateLimiter.from_preset("aggressive")

    return rate_limiter


def run_selected_modules(args, logger) -> Dict[str, list]:
    results = {}

    start_port, end_port = args.ports

    # Create rate limiter based on CLI arguments
    rate_limiter = create_rate_limiter(args)

    # Initialize generic ScanConfig
    config = ScanConfig(
        host=args.host,
        ports=(start_port, end_port),
        timeout=args.timeout,
        rate_limiter=rate_limiter,
        workers=getattr(args, "workers", 100),
        extras={
            "verify": not getattr(args, "no_verify", False),
            "ssl_port": getattr(args, "ssl_port", 443),
        },
    )

    modules_to_run = (
        args.modules if hasattr(args, "modules") and args.modules else ["tcp"]
    )

    for module_name in modules_to_run:
        scanner_class = ScannerRegistry.get_scanner(module_name)
        if scanner_class:
            scanner_instance = scanner_class()
            results[module_name] = scanner_instance.scan(config)
        else:
            logger.error(f"Unknown module '{module_name}' requested.")

    return results
