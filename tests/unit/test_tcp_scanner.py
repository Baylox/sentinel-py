from unittest.mock import MagicMock, patch

from scanner.core.config import ScanConfig
from scanner.core.tcp import TCPScanner


@patch("scanner.core.tcp.socket.socket")
def test_scan_ports_open(mock_socket_class):
    mock_socket = MagicMock()
    mock_socket.connect_ex.return_value = 0
    mock_socket_class.return_value.__enter__.return_value = mock_socket

    scanner = TCPScanner()
    config = ScanConfig(host="127.0.0.1", ports=(80, 80), timeout=0.1)
    result = scanner.scan(config)

    assert 80 in result["open_ports"]
    assert result["scan_results"][0]["status"] == "open"
    assert result["scan_results"][0]["port"] == 80


@patch("scanner.core.tcp.socket.socket")
def test_scan_ports_closed(mock_socket_class):
    mock_socket = MagicMock()
    mock_socket.connect_ex.return_value = 1
    mock_socket_class.return_value.__enter__.return_value = mock_socket

    scanner = TCPScanner()
    config = ScanConfig(host="127.0.0.1", ports=(81, 81), timeout=0.1)
    result = scanner.scan(config)

    assert 81 not in result["open_ports"]
    assert result["scan_results"][0]["status"] == "closed"
    assert result["scan_results"][0]["port"] == 81


@patch("scanner.core.tcp.socket.socket")
def test_scan_concurrent_preserves_port_order(mock_socket_class):
    """A multi-port concurrent scan must return results in ascending port order."""
    mock_socket = MagicMock()
    mock_socket.connect_ex.return_value = 0
    mock_socket_class.return_value.__enter__.return_value = mock_socket

    scanner = TCPScanner()
    config = ScanConfig(host="127.0.0.1", ports=(20, 30), timeout=0.1, workers=8)
    result = scanner.scan(config)

    scanned_ports = [r["port"] for r in result["scan_results"]]
    assert scanned_ports == list(range(20, 31))
    assert result["open_ports"] == list(range(20, 31))


@patch("scanner.core.tcp.socket.socket")
def test_scan_paces_submission_with_rate_limiter(mock_socket_class):
    """The rate limiter must be invoked once per port, even when concurrent."""
    mock_socket = MagicMock()
    mock_socket.connect_ex.return_value = 1
    mock_socket_class.return_value.__enter__.return_value = mock_socket

    rate_limiter = MagicMock()

    scanner = TCPScanner()
    config = ScanConfig(
        host="127.0.0.1",
        ports=(20, 24),
        timeout=0.1,
        workers=4,
        rate_limiter=rate_limiter,
    )
    scanner.scan(config)

    assert rate_limiter.wait.call_count == 5
