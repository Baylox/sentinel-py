"""
Advanced logging configuration for SentinelPy CLI.

Provides:
- Custom SUCCESS level (25)
- Context-aware logging with tags
- Rich console output with color themes
- Rotating file logs
- Clean, single-file maintainable API
"""

import logging
import shutil
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional, Any

try:
    from rich.logging import RichHandler
    from rich.console import Console
    from rich.theme import Theme
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# Define custom log level
SUCCESS = 25
logging.addLevelName(SUCCESS, "SUCCESS")

# Patch logger with .success()
def success(self, msg, *args, **kwargs):
    if self.isEnabledFor(SUCCESS):
        self._log(SUCCESS, msg, args, **kwargs)
logging.Logger.success = success

# Context tag filter
class ContextFilter(logging.Filter):
    def __init__(self, context: Optional[str] = None):
        super().__init__()
        self.context = context

    def filter(self, record: logging.LogRecord) -> bool:
        record.context = f"[{self.context}]" if self.context else "[]"
        return True

# Custom rich handler for console display
class CustomRichHandler(RichHandler):
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

# Setup logger
def setup_logger(logfile: Optional[str] = None) -> logging.Logger:
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    log_filename = logfile or "scanner.log"
    log_path = logs_dir / log_filename

    logger = logging.getLogger("sentinelpy")
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger  # Already configured

    # FILE format
    file_format = "[%(asctime)s] %(levelname)-8s | %(context)s %(message)s"
    date_format = "%d-%m-%Y %H:%M:%S"
    file_formatter = logging.Formatter(file_format, date_format)

    # CONSOLE handler with rich
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
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(file_formatter)

    # FILE handler
    file_handler = RotatingFileHandler(
        log_path, maxBytes=10 * 1024 * 1024,
        backupCount=5, encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)

    # Register handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# Contextual log wrapper
def log_with_context(
    logger: logging.Logger,
    level: int,
    msg: str,
    *args: Any,
    context: Optional[str] = None,
    **kwargs: Any
) -> None:
    context_filter = ContextFilter(context)
    logger.addFilter(context_filter)
    try:
        logger.log(level, msg, *args, **kwargs)
    finally:
        logger.removeFilter(context_filter)

# Util: clear log directory
def clear_logs() -> None:
    logs_dir = Path("logs")
    if logs_dir.exists():
        shutil.rmtree(logs_dir)
    logs_dir.mkdir(exist_ok=True)

# Util: display log file content
def show_logs(logfile: Optional[str] = None) -> str:
    log_filename = logfile or "scanner.log"
    log_path = Path("logs") / log_filename

    if not log_path.exists():
        return f"No log file found at {log_path}"
    
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading log file: {str(e)}"

