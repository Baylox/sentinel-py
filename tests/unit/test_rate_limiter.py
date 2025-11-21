"""Unit tests for the RateLimiter class."""

import time

import pytest

from scanner.utils.rate_limiter import RateLimiter


class TestRateLimiter:
    """Test suite for RateLimiter functionality."""

    def test_fixed_delay(self):
        """Test that fixed delay is applied correctly."""
        delay = 0.1
        limiter = RateLimiter(delay=delay, jitter=False)
        
        start = time.time()
        limiter.wait()
        elapsed = time.time() - start
        
        # Allow 20ms tolerance for system scheduling
        assert abs(elapsed - delay) < 0.02, f"Expected ~{delay}s, got {elapsed:.3f}s"

    def test_no_delay(self):
        """Test that zero delay means no waiting."""
        limiter = RateLimiter(delay=0)
        
        start = time.time()
        limiter.wait()
        elapsed = time.time() - start
        
        # Should be nearly instantaneous (< 10ms)
        assert elapsed < 0.01, f"Expected instant, got {elapsed:.3f}s"

    def test_jitter_randomization(self):
        """Test that jitter produces randomized delays."""
        delay = 0.1
        limiter = RateLimiter(delay=delay, jitter=True)
        
        delays = []
        for _ in range(5):
            start = time.time()
            limiter.wait()
            delays.append(time.time() - start)
        
        # With jitter, delays should be within 0.5x-2.0x of base delay
        for d in delays:
            assert delay * 0.5 <= d <= delay * 2.0, f"Delay {d:.3f}s outside jitter range"
        
        # Delays should not all be the same (variance check)
        assert len(set([round(d, 2) for d in delays])) > 1, "Jitter should produce varied delays"

    def test_preset_stealth(self):
        """Test stealth preset configuration."""
        limiter = RateLimiter.from_preset('stealth')
        
        assert limiter is not None
        assert limiter.delay == 1.0
        assert limiter.jitter is True

    def test_preset_normal(self):
        """Test normal preset configuration."""
        limiter = RateLimiter.from_preset('normal')
        
        assert limiter is not None
        assert limiter.delay == 0.05
        assert limiter.jitter is False

    def test_preset_aggressive(self):
        """Test aggressive preset configuration."""
        limiter = RateLimiter.from_preset('aggressive')
        
        assert limiter is not None
        assert limiter.delay == 0.01
        assert limiter.jitter is False

    def test_preset_none(self):
        """Test that 'none' preset returns None."""
        limiter = RateLimiter.from_preset('none')
        
        assert limiter is None

    def test_invalid_preset(self):
        """Test that invalid preset raises ValueError."""
        with pytest.raises(ValueError, match="Unknown preset"):
            RateLimiter.from_preset('invalid')

    def test_repr(self):
        """Test string representation."""
        limiter = RateLimiter(delay=0.05, jitter=False)
        repr_str = repr(limiter)
        
        assert "RateLimiter" in repr_str
        assert "0.05" in repr_str
        assert "req/s" in repr_str

    def test_none_preset_warning(self, caplog):
        """Test that 'none' preset logs a warning."""
        import logging
        with caplog.at_level(logging.WARNING):
            RateLimiter.from_preset('none')
        
        assert "DISABLED" in caplog.text
        assert "overload targets" in caplog.text
