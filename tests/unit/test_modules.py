"""Unit tests for scanner modules configuration."""

import logging
from argparse import Namespace

import pytest

from scanner.modules import create_rate_limiter
from scanner.utils.rate_limiter import RateLimiter


class TestCreateRateLimiter:
    """Test suite for create_rate_limiter function."""

    def test_custom_delay_override(self):
        """Test that custom delay overrides preset."""
        args = Namespace(delay=0.3, preset='normal', ports=(1, 100))
        limiter = create_rate_limiter(args)
        
        assert limiter is not None
        assert limiter.delay == 0.3
        assert limiter.jitter is False

    def test_normal_preset(self):
        """Test normal preset selection."""
        args = Namespace(delay=None, preset='normal', ports=(1, 100))
        limiter = create_rate_limiter(args)
        
        assert limiter is not None
        assert limiter.delay == 0.05

    def test_stealth_preset(self):
        """Test stealth preset selection."""
        args = Namespace(delay=None, preset='stealth', ports=(1, 100))
        limiter = create_rate_limiter(args)
        
        assert limiter is not None
        assert limiter.delay == 1.0
        assert limiter.jitter is True

    def test_none_preset_small_scan(self):
        """Test that 'none' preset is allowed for small scans."""
        args = Namespace(delay=None, preset='none', ports=(1, 100))
        limiter = create_rate_limiter(args)
        
        # Should be None for small scans
        assert limiter is None

    def test_none_preset_large_scan_enforces_safety(self, caplog):
        """Test that large scans enforce minimal rate limiting even with 'none'."""
        args = Namespace(delay=None, preset='none', ports=(1, 1500))
        
        with caplog.at_level(logging.WARNING):
            limiter = create_rate_limiter(args)
        
        # Should NOT be None - safety enforced
        assert limiter is not None
        assert limiter.delay == 0.01  # Aggressive preset
        
        # Check warning was logged
        assert "Large scan detected" in caplog.text
        assert "1500 ports" in caplog.text
        assert "Enforcing minimal rate limiting" in caplog.text

    def test_none_preset_exactly_1000_ports(self):
        """Test boundary: exactly 1000 ports should not trigger safety."""
        args = Namespace(delay=None, preset='none', ports=(1, 1000))
        limiter = create_rate_limiter(args)
        
        # Exactly 1000 ports should be allowed without rate limiting
        assert limiter is None

    def test_none_preset_1001_ports_triggers_safety(self):
        """Test boundary: 1001 ports should trigger safety."""
        args = Namespace(delay=None, preset='none', ports=(1, 1001))
        limiter = create_rate_limiter(args)
        
        # 1001 ports should trigger safety
        assert limiter is not None
        assert limiter.delay == 0.01  # Aggressive preset

    def test_default_preset_when_missing(self):
        """Test that 'normal' is used as default when preset is missing."""
        args = Namespace(delay=None, ports=(1, 100))
        # No 'preset' attribute
        limiter = create_rate_limiter(args)
        
        assert limiter is not None
        assert limiter.delay == 0.05  # Normal preset
