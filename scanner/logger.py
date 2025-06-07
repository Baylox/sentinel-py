"""
Advanced logging configuration for SentinelPy CLI.

This module provides a unified logging system with:
- Custom SUCCESS level (25)
- Context-aware logging with tags
- Rich console output with custom theme
- Rotating file logs
- Clean and maintainable API
"""

import logging
import shutil
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional, Dict, Any

try:
    from rich.logging import RichHandler
    from rich.console import Console
    from rich.theme import Theme
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# Custom log level
SUCCESS = 25
logging.addLevelName(SUCCESS, "SUCCESS")

def success(self, msg, *args, **kwargs):
    """Add success method to Logger class."""
    if self.isEnabledFor(SUCCESS):
        self._log(SUCCESS, msg, args, **kwargs)

logging.Logger.success = success

class ContextFilter(logging.Filter):
    """Filter to add context tags to log records."""
    
    def __init__(self, context: Optional[str] = None):
        super().__init__()
        self.context = context

    def filter(self, record: logging.LogRecord) -> bool:
        record.context = f"[{self.context}] " if self.context else ""
        return True

class CustomRichHandler(RichHandler):
    """Enhanced Rich handler with custom theme and context support."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.console = Console(theme=Theme({
            "logging.level.success": "bold green",
            "logging.level.info": "bold blue",
            "logging.level.warning": "bold yellow",
            "logging.level.error": "bold red",
            "logging.level.critical": "bold red reverse",
            "logging.context": "cyan",
        }))

    def get_level_text(self, record: logging.LogRecord) -> str:
        if record.levelno == SUCCESS:
            return "[bold green]SUCCESS[/bold green]"
        return super().get_level_text(record)

    def format(self, record: logging.LogRecord) -> str:
        if hasattr(record, 'context'):
            record.msg = f"{record.context}{record.msg}"
        return super().format(record)

def log_with_context(logger: logging.Logger, level: int, msg: str, *args, context: Optional[str] = None, **kwargs) -> None:
    """
    Log a message with context tag.
    
    Args:
        logger: Logger instance
        level: Log level
        msg: Message to log
        *args: Additional positional arguments for string formatting
        context: Optional context tag (e.g., "SCAN")
        **kwargs: Additional logging parameters
    """
    context_filter = ContextFilter(context)
    logger.addFilter(context_filter)
    try:
        logger.log(level, msg, *args, **kwargs)
    finally:
        logger.removeFilter(context_filter)

def setup_logger(logfile: Optional[str] = None) -> logging.Logger:
    """
    Configure and return a logger with console and file handlers.
    
    Args:
        logfile: Log filename. If None, uses 'scanner.log'
    
    Returns:
        logging.Logger: Configured logger
    """
    # Create logs directory
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
    
    # Log format for file handler
    file_format = "[%(asctime)s] %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    file_formatter = logging.Formatter(file_format, date_format)
    
    # Console handler (INFO level) with Rich if available
    if RICH_AVAILABLE:
        console_handler = CustomRichHandler(
            level=logging.INFO,
            rich_tracebacks=True,
            markup=True,
            show_time=True,
            show_path=False,
            enable_link_path=False,
            show_level=True
        )
    else:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(file_formatter)
    
    # File handler (DEBUG level) with rotation
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    
    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

def clear_logs() -> None:
    """Clear all log files from the logs directory."""
    logs_dir = Path("logs")
    if logs_dir.exists():
        shutil.rmtree(logs_dir)
        logs_dir.mkdir(exist_ok=True)

def show_logs(logfile: Optional[str] = None) -> str:
    """
    Read and return the contents of a log file.
    
    Args:
        logfile: Log filename to read. If None, reads 'scanner.log'
    
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
