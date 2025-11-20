import socket
from unittest.mock import MagicMock, patch

import pytest

from scanner.core.ssl import SSLScanner


@pytest.fixture
def ssl_scanner():
    """Fixture for SSLScanner instance."""
    return SSLScanner(timeout=2.0, verify=True)


@patch("scanner.core.ssl.socket.create_connection")
@patch("scanner.core.ssl.ssl.create_default_context")
def test_ssl_scanner_valid_certificate(mock_ssl_context, mock_socket, ssl_scanner):
    """Test SSL scanner with a valid certificate."""
    # Mock certificate data with correct date format
    mock_cert = {
        "subject": ((("commonName", "example.com"),),),
        "issuer": ((("commonName", "Let's Encrypt"),),),
        "notBefore": "Jan  1 00:00:00 2024 GMT",  # Double space is important
        "notAfter": "Dec 31 23:59:59 2025 GMT",
    }

    # Setup mocks
    mock_ssock = MagicMock()
    mock_ssock.getpeercert.return_value = mock_cert
    
    mock_sock = MagicMock()
    mock_sock.__enter__ = MagicMock(return_value=mock_ssock)
    mock_sock.__exit__ = MagicMock(return_value=False)
    
    mock_context = MagicMock()
    mock_context.wrap_socket.return_value = mock_sock
    mock_ssl_context.return_value = mock_context

    # Run scan
    result = ssl_scanner.scan("example.com", 443)

    # Assertions
    assert result["ok"] is True
    assert result["issued_to"] == "example.com"
    assert result["issued_by"] == "Let's Encrypt"
    assert "valid_from" in result
    assert "valid_until" in result
    # Don't assert on expired as it depends on current date


@patch("scanner.core.ssl.socket.create_connection")
def test_ssl_scanner_no_certificate(mock_socket, ssl_scanner):
    """Test SSL scanner when no certificate is presented."""
    # Mock empty certificate
    mock_ssock = MagicMock()
    mock_ssock.getpeercert.return_value = None

    with patch("scanner.core.ssl.ssl.create_default_context") as mock_ssl_context:
        mock_context = MagicMock()
        mock_context.wrap_socket.return_value.__enter__.return_value = mock_ssock
        mock_ssl_context.return_value = mock_context

        # Run scan
        result = ssl_scanner.scan("example.com", 443)

        # Assertions
        assert result["ok"] is False
        assert "error" in result
        assert "No certificate" in result["error"]


@patch("scanner.core.ssl.socket.create_connection")
def test_ssl_scanner_connection_error(mock_socket, ssl_scanner):
    """Test SSL scanner when connection fails."""
    # Mock connection error
    mock_socket.side_effect = OSError("Connection refused")

    # Run scan
    result = ssl_scanner.scan("invalid-host.local", 443)

    # Assertions
    assert result["ok"] is False
    assert "error" in result
    assert "Socket error" in result["error"]
