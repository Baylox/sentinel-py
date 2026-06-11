from unittest.mock import MagicMock, patch

from scanner.core.tcp import TCPScanner
from scanner.core.config import ScanConfig


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
