import pytest
from unittest.mock import patch, MagicMock
from scanner.core.scanner import PortScanner

@patch("scanner.core.scanner.socket.socket")
def test_scan_ports_open(mock_socket_class):
    mock_socket = MagicMock()
    mock_socket.connect_ex.return_value = 0 
    mock_socket_class.return_value.__enter__.return_value = mock_socket

    scanner = PortScanner(timeout=0.1)
    result = scanner.scan("127.0.0.1", "80-80")

    assert 80 in result["open_ports"]
    assert result["scan_results"][0]["status"] == "open"
    assert result["scan_results"][0]["port"] == 80

@patch("scanner.core.scanner.socket.socket")
def test_scan_ports_closed(mock_socket_class):
    mock_socket = MagicMock()
    mock_socket.connect_ex.return_value = 1  
    mock_socket_class.return_value.__enter__.return_value = mock_socket

    scanner = PortScanner()
    result = scanner.scan("127.0.0.1", "81-81")

    assert 81 not in result["open_ports"]
    assert result["scan_results"][0]["status"] == "closed"
    assert result["scan_results"][0]["port"] == 81

