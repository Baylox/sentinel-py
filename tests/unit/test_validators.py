import pytest
from scanner.cli.parser import (
    validate_port_range,
    validate_host,
    validate_timeout,
    CLIValidationError,
)

@pytest.mark.parametrize(
    "ports,expected", [("22-22", (22, 22)), ("1-65535", (1, 65535))]
)
def test_validate_port_range_ok(ports, expected):
    assert validate_port_range(ports) == expected


@pytest.mark.parametrize("ports", ["0-1", "22-21", "abc", "70000-80000"])
def test_validate_port_range_error(ports):
    with pytest.raises(CLIValidationError):
        validate_port_range(ports)


@pytest.mark.parametrize("host", ["127.0.0.1", "localhost", "example.com"])
def test_validate_host_ok(host):
    assert validate_host(host) == host


@pytest.mark.parametrize("tout", [0.5, 5.0, 10.0])
def test_validate_timeout_ok(tout):
    assert validate_timeout(tout) == tout


@pytest.mark.parametrize("tout", [0.01, 20.0])
def test_validate_timeout_error(tout):
    with pytest.raises(CLIValidationError):
        validate_timeout(tout)
