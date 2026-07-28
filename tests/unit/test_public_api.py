"""Tests for the public ``scanner.scan_ports`` convenience API."""

from unittest.mock import MagicMock, patch

import pytest

import scanner as scanner_pkg
from scanner import PortRangeError, ScanConfig, scan_ports


@patch("scanner.core.tcp.socket.gethostbyname")
@patch("scanner.core.tcp.socket.socket")
def test_scan_ports_open(mock_socket_class, mock_resolve):
    """scan_ports() wires a host/port-range string through TCPScanner."""
    mock_resolve.return_value = "127.0.0.1"
    mock_socket = MagicMock()
    mock_socket.connect_ex.return_value = 0
    mock_socket_class.return_value.__enter__.return_value = mock_socket

    result = scan_ports("127.0.0.1", "80-80", timeout=0.1)

    assert 80 in result["open_ports"]
    assert result["scan_results"][0]["status"] == "open"
    assert result["scan_results"][0]["port"] == 80


def test_scan_ports_invalid_range():
    """An invalid port range surfaces as PortRangeError."""
    with pytest.raises(PortRangeError):
        scan_ports("127.0.0.1", "not-a-range")


@patch("scanner.TCPScanner")
def test_scan_ports_builds_scan_config(mock_scanner_class):
    """The range string is parsed into a ScanConfig handed to TCPScanner.scan()."""
    scan_ports("127.0.0.1", "20-25", timeout=1.5)

    (config,) = mock_scanner_class.return_value.scan.call_args.args
    assert isinstance(config, ScanConfig)
    assert config.host == "127.0.0.1"
    assert config.ports == (20, 25)
    assert config.timeout == 1.5


def test_public_names_are_exported():
    """Names used by examples/ must stay reachable from the package root."""
    for name in ("scan_ports", "ScanConfig", "TCPScanner", "PortScannerError"):
        assert name in scanner_pkg.__all__
        assert hasattr(scanner_pkg, name)
