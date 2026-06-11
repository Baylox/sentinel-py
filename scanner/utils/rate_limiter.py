"""Rate limiting utility for SentinelPy scanners.

This module provides a simple rate limiter to control the speed of scanning operations,
preventing target overload and reducing detectability.
"""

import logging
import random
import time
from typing import Optional

logger = logging.getLogger(__name__)


class RateLimiter:
    """Controls the rate of requests to prevent target overload.
    
    Implements configurable delays between requests with optional jitter
    for stealth scanning. Simple implementation using time.sleep().
    
    Attributes:
        delay: Fixed delay between requests in seconds
        jitter: Whether to randomize delays (range: 0.5x-2.0x)
    """
    
    def __init__(self, delay: float = 0.05, jitter: bool = False):
        """Initialize the rate limiter.
        
        Args:
            delay: Delay between requests in seconds (default: 0.05s = 50ms ~20 req/s)
            jitter: Enable delay randomization for stealth (hardcoded range: 0.5x-2.0x)
        """
        self.delay = delay
        self.jitter = jitter
        self._jitter_min = 0.5
        self._jitter_max = 2.0
        
        logger.debug(
            f"RateLimiter initialized: delay={delay}s (~{1/delay if delay > 0 else 'unlimited'} req/s), "
            f"jitter={'enabled' if jitter else 'disabled'}"
        )
    
    def wait(self) -> None:
        """Apply the configured delay.
        
        Sleeps for the configured duration. If jitter is enabled,
        the delay is randomized within the range [delay*0.5, delay*2.0].
        """
        if self.delay <= 0:
            return
        
        actual_delay = self.delay
        
        if self.jitter:
            # Apply jitter: randomize within range
            multiplier = random.uniform(self._jitter_min, self._jitter_max)
            actual_delay = self.delay * multiplier
            logger.debug(f"Rate limit: waiting {actual_delay:.3f}s (jittered from {self.delay:.3f}s)")
        else:
            logger.debug(f"Rate limit: waiting {actual_delay:.3f}s")
        
        time.sleep(actual_delay)
    
    @classmethod
    def from_preset(cls, mode: str) -> Optional['RateLimiter']:
        """Create a rate limiter from a preset mode.
        
        Args:
            mode: Preset name - 'stealth', 'normal', 'aggressive', or 'none'
        
        Returns:
            RateLimiter instance or None if mode='none'
        
        Raises:
            ValueError: If mode is not recognized
        """
        presets = {
            'stealth': cls(delay=1.0, jitter=True),  # ~1s avg (500ms-2s range)
            'normal': cls(delay=0.05, jitter=False),  # 50ms (~20 req/s)
            'aggressive': cls(delay=0.01, jitter=False),  # 10ms (~100 req/s)
            'none': None,  # No rate limiting
        }
        
        if mode not in presets:
            raise ValueError(
                f"Unknown preset '{mode}'. "
                f"Valid options: {', '.join(presets.keys())}"
            )
        
        limiter = presets[mode]
        if limiter:
            logger.info(f"Rate limiter preset '{mode}' activated: {limiter}")
        else:
            logger.warning(
                "Rate limiting DISABLED (preset='none'). "
                "This may overload targets and is detectable. "
                "Only use for local/authorized testing!"
            )
        
        return limiter
    
    def __repr__(self) -> str:
        """String representation for logging."""
        jitter_str = f" with jitter [{self._jitter_min}x-{self._jitter_max}x]" if self.jitter else ""
        rps = f"~{1/self.delay:.1f} req/s" if self.delay > 0 else "unlimited"
        return f"RateLimiter(delay={self.delay}s, {rps}{jitter_str})"
