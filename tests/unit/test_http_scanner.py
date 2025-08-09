from unittest.mock import MagicMock, patch

from scanner.core.http import HTTPScanner


@patch("scanner.core.http.requests.get")
def test_http_scanner_success(mock_get):
    """Test HTTPScanner when server replies 200 OK."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {"Server": "MockServer", "Content-Type": "text/html"}
    mock_response.ok = True
    mock_get.return_value = mock_response

    scanner = HTTPScanner(timeout=1)
    result = scanner.scan("testserver.com", [8080])

    assert result["open_ports"] == [8080]
    assert len(result["scan_results"]) == 1
    assert result["scan_results"][0]["status_code"] == 200
    assert result["scan_results"][0]["server"] == "Mockserver"
    assert result["scan_results"][0]["url"] == "http://testserver.com:8080/"


@patch("scanner.core.http.requests.get")
def test_http_scanner_error(mock_get):
    """Test HTTPScanner handles request exceptions."""
    mock_get.side_effect = Exception("Timeout or connection error")

    scanner = HTTPScanner(timeout=1)
    result = scanner.scan("badhost", [1234])

    assert result["open_ports"] == []
    assert len(result["scan_results"]) == 1
    assert "error" in result["scan_results"][0]
    assert result["scan_results"][0]["url"] == "http://badhost:1234/"
