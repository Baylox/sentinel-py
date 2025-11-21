"""File path sanitization utilities to prevent path traversal attacks."""

import os
from pathlib import Path
from typing import Optional


class PathTraversalError(Exception):
    """Raised when a path traversal attempt is detected."""
    pass


def sanitize_filepath(filepath: str, base_dir: Optional[str] = None, allow_absolute: bool = False) -> str:
    """Sanitize a file path to prevent path traversal attacks.
    
    This function ensures that:
    1. The path doesn't contain path traversal sequences (../, ..\)
    2. The resolved path stays within the allowed base directory
    3. Dangerous characters are detected
    
    Args:
        filepath: The file path to sanitize
        base_dir: Base directory to restrict paths to. If None, uses current working directory.
        allow_absolute: Whether to allow absolute paths. If False, converts to relative.
    
    Returns:
        str: Sanitized absolute path
    
    Raises:
        PathTraversalError: If path traversal is detected
        ValueError: If the path is invalid or empty
    
    Examples:
        >>> sanitize_filepath("results.json")
        '/current/dir/results.json'
        
        >>> sanitize_filepath("../etc/passwd")  # Raises PathTraversalError
        
        >>> sanitize_filepath("subdir/report.json", base_dir="/app/exports")
        '/app/exports/subdir/report.json'
    """
    if not filepath or not filepath.strip():
        raise ValueError("File path cannot be empty")
    
    filepath = filepath.strip()
    
    # Detect obvious path traversal patterns
    # Check for ../ or ..\ before normalization
    dangerous_patterns = ['../', '..\\', '/../', '\\..\\']
    for pattern in dangerous_patterns:
        if pattern in filepath:
            raise PathTraversalError(
                f"Path traversal detected in '{filepath}': contains '{pattern}'"
            )
    
    # Convert to Path object for proper handling
    try:
        path = Path(filepath)
    except (ValueError, OSError) as e:
        raise ValueError(f"Invalid file path '{filepath}': {e}")
    
    # Determine base directory
    if base_dir is None:
        base_dir = os.getcwd()
    else:
        base_dir = os.path.abspath(base_dir)
    
    base_path = Path(base_dir)
    
    # If path is absolute and we don't allow it, make it relative
    if path.is_absolute() and not allow_absolute:
        # Extract just the filename (last component)
        path = Path(path.name)
    
    # Build the full path
    # If path is relative, join with base_dir
    if not path.is_absolute():
        full_path = base_path / path
    else:
        full_path = path
    
    # Normalize the path (resolve .. and . components) without following symlinks
    # Use os.path.normpath for this as resolve() requires the path to exist
    full_path = Path(os.path.normpath(str(full_path)))
    
    # Make it absolute if it isn't already
    if not full_path.is_absolute():
        full_path = Path(os.path.abspath(str(full_path)))
    
    # Security check: ensure the resolved path is within base_dir
    # (skip this check if absolute paths are explicitly allowed)
    if not allow_absolute:
        base_resolved = Path(os.path.abspath(str(base_path)))
        try:
            full_path.relative_to(base_resolved)
        except ValueError:
            raise PathTraversalError(
                f"Path '{filepath}' resolves to '{full_path}' which is outside "
                f"the allowed directory '{base_resolved}'"
            )
    
    # Additional check for null bytes (can be used in path injection)
    if '\x00' in str(full_path):
        raise PathTraversalError(f"Null byte detected in path: {filepath}")
    
    return str(full_path)


def sanitize_log_path(logfile: str) -> str:
    """Sanitize a log file path, restricting it to the logs/ directory.
    
    Args:
        logfile: Log file name or path
    
    Returns:
        str: Sanitized path within logs/ directory
    
    Raises:
        PathTraversalError: If path traversal is detected
    """
    # Get the project root (parent of scanner package)
    scanner_dir = Path(__file__).parent.parent
    logs_dir = scanner_dir.parent / 'logs'
    
    # Create logs directory if it doesn't exist
    logs_dir.mkdir(exist_ok=True)
    
    return sanitize_filepath(logfile, base_dir=str(logs_dir), allow_absolute=False)


def sanitize_export_path(export_file: str) -> str:
    """Sanitize an export file path, restricting it to the exports/ directory.
    
    Args:
        export_file: Export file name or path
    
    Returns:
        str: Sanitized path within exports/ directory
    
    Raises:
        PathTraversalError: If path traversal is detected
    """
    # Get the project root
    scanner_dir = Path(__file__).parent.parent
    exports_dir = scanner_dir.parent / 'exports'
    
    # Create exports directory if it doesn't exist
    exports_dir.mkdir(exist_ok=True)
    
    return sanitize_filepath(export_file, base_dir=str(exports_dir), allow_absolute=False)
