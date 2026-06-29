# tests/test_cli_parser.py
import pytest

from scanner.cli.parser import parse_args


def test_parse_minimal():
    """Basic parse: host + port-range only."""
    ns = parse_args(["localhost", "20-30"])
    assert ns.host == "localhost"
    # validate tuple conversion after custom validation
    assert ns.ports == (20, 30)
    # default timeout should remain unchanged
    assert ns.timeout == 0.5
    # default worker count should remain unchanged
    assert ns.workers == 100


def test_parse_workers_valid():
    """A valid --workers value is accepted."""
    ns = parse_args(["localhost", "20-30", "--workers", "50"])
    assert ns.workers == 50


@pytest.mark.parametrize("value", ["0", "1001", "-5"])
def test_parse_workers_out_of_range(value):
    """Out-of-range --workers values are rejected by the parser."""
    with pytest.raises(SystemExit):
        parse_args(["localhost", "20-30", "--workers", value])


def test_parse_json_flag(tmp_path):
    """Parse --json flag: path is sanitized to exports/ and port tuple captured."""
    json_file = tmp_path / "out.json"
    ns = parse_args(["127.0.0.1", "80-80", "--json", str(json_file)])

    # Path should be sanitized to exports/out.json (just the filename)
    from pathlib import Path

    assert Path(ns.json).name == "out.json"
    assert "exports" in Path(ns.json).parts
    assert ns.ports == (80, 80)  # tuple after validation
