# tests/test_cli_parser.py
from scanner.cli.parser import parse_args


def test_parse_minimal():
    """Basic parse: host + port-range only."""
    ns = parse_args(["localhost", "20-30"])
    assert ns.host == "localhost"
    # validate tuple conversion after custom validation
    assert ns.ports == (20, 30)
    # default timeout should remain unchanged
    assert ns.timeout == 0.5


def test_parse_json_flag(tmp_path):
    """Parse with --json flag; ensure file path and port tuple are captured."""
    json_file = tmp_path / "out.json"
    ns = parse_args(["127.0.0.1", "80-80", "--json", str(json_file)])

    assert ns.json == str(json_file)  # CLI stores the provided filename
    assert ns.ports == (80, 80)  # tuple after validation
