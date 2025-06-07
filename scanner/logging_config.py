import logging
import shutil
from pathlib import Path
from typing import Optional

def clear_logs() -> None:
    """
    Clear all log files from the logs directory.
    """
    logs_dir = Path("logs")
    if logs_dir.exists():
        shutil.rmtree(logs_dir)
        logs_dir.mkdir(exist_ok=True)

def show_logs(logfile: Optional[str] = None) -> str:
    """
    Read and return the contents of a log file.
    
    Args:
        logfile (str | None): Log filename to read. If None, reads 'scanner.log'
    
    Returns:
        str: Contents of the log file
    """
    log_filename = logfile if logfile else "scanner.log"
    log_path = Path("logs") / log_filename
    
    if not log_path.exists():
        return f"No log file found at {log_path}"
    
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading log file: {str(e)}"

def setup_logger(logfile: Optional[str] = None) -> logging.Logger:
    """
    Configure and return a logger with console and file handlers.
    
    Args:
        logfile (str | None): Log filename. If None, uses 'scanner.log'
    
    Returns:
        logging.Logger: Configured logger
    """
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Configure log filename
    log_filename = logfile if logfile else "scanner.log"
    log_path = logs_dir / log_filename
    
    # Create logger
    logger = logging.getLogger("sentinelpy")
    logger.setLevel(logging.DEBUG)
    
    # Avoid multiple handlers
    if logger.handlers:
        return logger
    
    # Log format
    log_format = "[%(asctime)s] %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(log_format, date_format)
    
    # Console handler (INFO level)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # File handler (DEBUG level)
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger