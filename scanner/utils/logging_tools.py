import shutil
from pathlib import Path
from typing import Optional


def clear_logs() -> None:
    """
    Remove all log files by deleting and recreating the logs directory.
    """
    logs_dir = Path("logs")
    if logs_dir.exists():
        shutil.rmtree(logs_dir)
    logs_dir.mkdir(exist_ok=True)


def show_logs(logfile: Optional[str] = None) -> str:
    """
    Read and return the content of the specified log file.

    Args:
        logfile: Optional log file name. Defaults to 'scanner.log' in 'logs/'.

    Returns:
        str: Contents of the log file or error message.
    """
    log_filename = logfile or "scanner.log"
    log_path = Path("logs") / log_filename

    if not log_path.exists():
        return f"No log file found at {log_path}"

    try:
        with open(log_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading log file: {str(e)}"
