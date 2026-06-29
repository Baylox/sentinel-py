from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple


@dataclass
class ScanConfig:
    """
    Standard configuration for a port/vulnerability scan.

    This class unifies the parameters passed to all scanner modules.
    """

    host: str
    ports: Tuple[int, int]
    timeout: float = 0.5
    rate_limiter: Optional[Any] = None
    workers: int = 100
    extras: Dict[str, Any] = field(default_factory=dict)
