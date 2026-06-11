import json
from pathlib import Path

import pytest

from scanner.utils.exporter import export_to_json, load_json


@pytest.fixture
def sample_results():
    """Fixture for sample scan results."""
    return {
        "tcp": {
            "open_ports": [22, 80, 443],
            "scan_results": [
                {"port": 22, "status": "open", "service": "ssh"},
                {"port": 80, "status": "open", "service": "http"},
                {"port": 443, "status": "open", "service": "https"},
            ],
        }
    }


def test_export_to_json_creates_file(tmp_path, sample_results, monkeypatch):
    """Test that export_to_json creates a valid JSON file."""
    # Patch EXPORT_DIR to use tmp_path
    from scanner.utils import exporter
    monkeypatch.setattr(exporter, "EXPORT_DIR", tmp_path)
    
    output_file = "test_export.json"

    # Export results
    export_to_json(sample_results, output_file)

    # Verify file exists
    expected_path = tmp_path / output_file
    assert expected_path.exists()

    # Verify content
    with open(expected_path, "r") as f:
        loaded_data = json.load(f)

    assert loaded_data == sample_results
    assert loaded_data["tcp"]["open_ports"] == [22, 80, 443]


def test_load_json_reads_file(tmp_path, sample_results):
    """Test that load_json correctly reads a JSON file."""
    test_file = tmp_path / "test_load.json"

    # Write test data
    with open(test_file, "w") as f:
        json.dump(sample_results, f)

    # Load data
    loaded_data = load_json(str(test_file))

    # Verify
    assert loaded_data == sample_results
    assert loaded_data["tcp"]["open_ports"] == [22, 80, 443]
