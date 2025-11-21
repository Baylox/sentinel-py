import csv
import os
import tempfile
from pathlib import Path
from scanner.utils.exporter import export_to_csv

def test_export_to_csv_creates_file():
    """Test that export_to_csv creates a file with the correct content."""
    # Setup
    data = {
        "tcp": {
            "scan_results": [
                {"port": 80, "status": "open", "service": "http", "banner": "nginx"},
                {"port": 22, "status": "open", "service": "ssh", "banner": "OpenSSH"},
            ]
        }
    }
    host = "example.com"
    
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = "test_export.csv"
        # Temporarily override EXPORT_DIR for testing
        import scanner.utils.exporter
        original_export_dir = scanner.utils.exporter.EXPORT_DIR
        scanner.utils.exporter.EXPORT_DIR = Path(tmpdir)
        
        try:
            # Execute
            export_to_csv(data, host, filename)
            
            # Verify
            file_path = Path(tmpdir) / filename
            assert file_path.exists()
            
            with open(file_path, "r", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                rows = list(reader)
                
                # Check header
                assert rows[0] == ["host", "port", "status", "service", "banner"]
                
                # Check data
                assert len(rows) == 3
                assert rows[1] == ["example.com", "80", "open", "http", "nginx"]
                assert rows[2] == ["example.com", "22", "open", "ssh", "OpenSSH"]
                
        finally:
            # Cleanup
            scanner.utils.exporter.EXPORT_DIR = original_export_dir

def test_export_to_csv_handles_missing_fields():
    """Test that export_to_csv handles missing fields gracefully."""
    # Setup
    data = {
        "tcp": {
            "scan_results": [
                {"port": 80, "status": "open"}, # Missing service and banner
            ]
        }
    }
    host = "example.com"
    
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = "test_missing.csv"
        import scanner.utils.exporter
        original_export_dir = scanner.utils.exporter.EXPORT_DIR
        scanner.utils.exporter.EXPORT_DIR = Path(tmpdir)
        
        try:
            export_to_csv(data, host, filename)
            
            file_path = Path(tmpdir) / filename
            with open(file_path, "r", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                rows = list(reader)
                
                assert rows[1] == ["example.com", "80", "open", "N/A", ""]
                
        finally:
            scanner.utils.exporter.EXPORT_DIR = original_export_dir
