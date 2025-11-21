"""Unit tests for path sanitization utilities."""

import os
from pathlib import Path

import pytest

from scanner.utils.path_sanitizer import (
    PathTraversalError,
    sanitize_export_path,
    sanitize_filepath,
    sanitize_log_path,
)


class TestSanitizeFilepath:
    """Test suite for sanitize_filepath function."""

    def test_simple_filename(self):
        """Test sanitization of a simple filename."""
        result = sanitize_filepath("report.json", base_dir="/app/exports")
        assert result == str(Path("/app/exports/report.json").resolve())

    def test_path_traversal_dots_slash(self):
        """Test that ../ path traversal is detected."""
        with pytest.raises(PathTraversalError, match="Path traversal detected"):
            sanitize_filepath("../../../etc/passwd")

    def test_path_traversal_dots_backslash(self):
        """Test that ..\\ path traversal is detected."""
        with pytest.raises(PathTraversalError, match="Path traversal detected"):
            sanitize_filepath("..\\..\\windows\\system32")

    def test_path_traversal_middle_of_path(self):
        """Test that path traversal in the middle is detected."""
        with pytest.raises(PathTraversalError, match="Path traversal detected"):
            sanitize_filepath("safe/../../../etc/passwd")

    def test_subdir_allowed(self):
        """Test that subdirectories are allowed."""
        result = sanitize_filepath("logs/app.log", base_dir="/var")
        # Cross-platform: use Path for comparison
        result_path = Path(result)
        assert "logs" in result_path.parts
        assert result_path.name == "app.log"

    def test_empty_path(self):
        """Test that empty paths are rejected."""
        with pytest.raises(ValueError, match="cannot be empty"):
            sanitize_filepath("")

    def test_whitespace_only(self):
        """Test that whitespace-only paths are rejected."""
        with pytest.raises(ValueError, match="cannot be empty"):
            sanitize_filepath("   ")

    def test_null_byte_injection(self):
        """Test that null bytes are detected."""
        # Note: This test depends on the string containing actual null byte
        with pytest.raises(PathTraversalError, match="Null byte"):
            sanitize_filepath("file.txt\x00.jpg")

    def test_absolute_path_converted_to_relative(self):
        """Test that absolute paths are converted when allow_absolute=False."""
        result = sanitize_filepath("/etc/passwd", base_dir="/app", allow_absolute=False)
        # Should extract just the filename and place in base_dir
        result_path = Path(result)
        assert result_path.name == "passwd"

    def test_absolute_path_allowed(self):
        """Test that absolute paths work when allow_absolute=True."""
        # This should resolve to an absolute path
        result = sanitize_filepath("/tmp/test.log", allow_absolute=True)
        assert os.path.isabs(result)

    def test_base_dir_default_to_cwd(self):
        """Test that base_dir defaults to current working directory."""
        result = sanitize_filepath("test.txt")
        assert Path(result).parent == Path(os.getcwd()).resolve()

    def test_escaped_traversal_blocked(self):
        """Test various escaped path traversal attempts."""
        dangerous_paths = [
            "test/../../secret.txt",
            "..\\..\\secret.txt",
            "test/../../../etc/passwd",
        ]
        
        for path in dangerous_paths:
            with pytest.raises(PathTraversalError):
                sanitize_filepath(path, base_dir="/app")


class TestSanitizeLogPath:
    """Test suite for sanitize_log_path function."""

    def test_simple_log_file(self):
        """Test sanitization of a simple log filename."""
        result = sanitize_log_path("app.log")
        result_path = Path(result)
        assert result_path.name == "app.log"
        assert "logs" in result_path.parts

    def test_log_path_traversal_blocked(self):
        """Test that path traversal is blocked for log files."""
        with pytest.raises(PathTraversalError):
            sanitize_log_path("../etc/passwd")

    def test_log_subdir_allowed(self):
        """Test that subdirectories within logs/ are allowed."""
        result = sanitize_log_path("app/debug.log")
        result_path = Path(result)
        assert result_path.name == "debug.log"
        assert "logs" in result_path.parts
        assert "app" in result_path.parts

    def test_log_absolute_path_converted(self):
        """Test that absolute paths are converted to relative for logs."""
        result = sanitize_log_path("/var/log/system.log")
        result_path = Path(result)
        assert result_path.name == "system.log"
        assert "logs" in result_path.parts


class TestSanitizeExportPath:
    """Test suite for sanitize_export_path function."""

    def test_simple_export_file(self):
        """Test sanitization of a simple export filename."""
        result = sanitize_export_path("results.json")
        result_path = Path(result)
        assert result_path.name == "results.json"
        assert "exports" in result_path.parts

    def test_export_path_traversal_blocked(self):
        """Test that path traversal is blocked for export files."""
        with pytest.raises(PathTraversalError):
            sanitize_export_path("../../secret/data.json")

    def test_export_subdir_allowed(self):
        """Test that subdirectories within exports/ are allowed."""
        result = sanitize_export_path("reports/scan_2024.json")
        result_path = Path(result)
        assert result_path.name == "scan_2024.json"
        assert "exports" in result_path.parts
        assert "reports" in result_path.parts

    def test_export_absolute_path_converted(self):
        """Test that absolute paths are converted for exports."""
        result = sanitize_export_path("/tmp/output.json")
        result_path = Path(result)
        assert result_path.name == "output.json"
        assert "exports" in result_path.parts


class TestPathTraversalRealWorld:
    """Test real-world path traversal attack scenarios."""

    def test_windows_path_traversal(self):
        """Test Windows-style path traversal."""
        attacks = [
            "..\\..\\..\\windows\\system32\\config\\sam",
            "test\\..\\..\\secret.txt",
        ]
        
        for attack in attacks:
            with pytest.raises(PathTraversalError):
                # Use a Windows-style base on Windows, Unix-style otherwise
                base = "C:\\app" if os.name == 'nt' else "/app"
                sanitize_filepath(attack, base_dir=base)

    def test_unix_path_traversal(self):
        """Test Unix-style path traversal."""
        attacks = [
            "../../../etc/shadow",
            "logs/../../../root/.ssh/id_rsa",
        ]
        
        for attack in attacks:
            with pytest.raises(PathTraversalError):
                sanitize_filepath(attack, base_dir="/app")

    def test_mixed_separators(self):
        """Test mixed path separators (potential bypass attempt)."""
        with pytest.raises(PathTraversalError):
            sanitize_filepath("test/../..\\secret", base_dir="/app")

    def test_url_encoded_dots(self):
        """Test that encoded dots in filenames are handled safely."""
        # The filename itself is safe, but let's ensure it doesn't cause issues
        result = sanitize_filepath("file%2E%2Etxt", base_dir="/app")
        result_path = Path(result)
        assert result_path.name == "file%2E%2Etxt"

    def test_double_dot_in_filename(self):
        """Test that files with '..' in their name (but not as dir separator) work."""
        # Note: This is tricky - "file..txt" as a filename should be OK
        # But "file../secret" should not
        result = sanitize_filepath("backup..2024.tar.gz", base_dir="/app")
        assert Path(result).name == "backup..2024.tar.gz"
