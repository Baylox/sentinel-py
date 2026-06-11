import logging
import shutil
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Optional

try:
    from rich.console import Console
    from rich.logging import RichHandler
    from rich.theme import Theme

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# Custom log level: SUCCESS (between INFO and WARNING)
SUCCESS = 25
logging.addLevelName(SUCCESS, "SUCCESS")


# Add success() method to Logger
def success(self, msg, *args, **kwargs):
    if self.isEnabledFor(SUCCESS):
        self._log(SUCCESS, msg, args, **kwargs)


logging.Logger.success = success


# Filter to inject context tags into log records
class ContextFilter(logging.Filter):
    def __init__(self, context: Optional[str] = None):
        super().__init__()
        self.context = context

    def filter(self, record: logging.LogRecord) -> bool:
        record.context = f"[{self.context}]" if self.context else "[]"
        return True


# Rich console handler with custom theme and SUCCESS support
class CustomRichHandler(RichHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.console = Console(
            theme=Theme(
                {
                    "logging.level.success": "bold green",
                    "logging.level.info": "bold blue",
                    "logging.level.warning": "bold yellow",
                    "logging.level.error": "bold red",
                    "logging.level.critical": "bold red reverse",
                    "logging.context": "cyan",
                }
            )
        )

    def get_level_text(self, record: logging.LogRecord) -> str:
        if record.levelno == SUCCESS:
            return "[bold green]SUCCESS[/bold green]"
        return super().get_level_text(record)


# Main logger setup function
def setup_logger(logfile: Optional[str] = None) -> logging.Logger:
    logger = logging.getLogger("sentinelpy")
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger  # Prevent duplicate handlers

    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    log_filename = logfile or "scanner.log"
    log_path = logs_dir / log_filename

    file_format = "[%(asctime)s] %(levelname)-8s | %(context)s %(message)s"
    date_format = "%d-%m-%Y %H:%M:%S"
    file_formatter = logging.Formatter(file_format, date_format)

    # Console handler (Rich if available)
    if RICH_AVAILABLE:
        console_handler = CustomRichHandler(
            level=logging.INFO,
            rich_tracebacks=True,
            markup=True,
            show_time=True,
            show_path=False,
            enable_link_path=False,
            show_level=True,
        )
    else:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(file_formatter)

    # Rotating file handler for persistent logs
    file_handler = RotatingFileHandler(
        log_path, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# Log with contextual tag
def log_with_context(
    logger: logging.Logger,
    level: int,
    msg: str,
    *args: Any,
    context: Optional[str] = None,
    **kwargs: Any,
) -> None:
    context_filter = ContextFilter(context)
    logger.addFilter(context_filter)
    try:
        logger.log(level, msg, *args, **kwargs)
    finally:
        logger.removeFilter(context_filter)


# Utility: clear the entire logs directory
def clear_logs() -> None:
    logs_dir = Path("logs")
    if logs_dir.exists():
        shutil.rmtree(logs_dir)
    logs_dir.mkdir(exist_ok=True)


# Utility: read and return the content of the current log file
def show_logs(logfile: Optional[str] = None) -> str:
    log_filename = logfile or "scanner.log"
    log_path = Path("logs") / log_filename

    if not log_path.exists():
        return f"No log file found at {log_path}"

    try:
        with open(log_path, "r", encoding="utf-8") as f:
            return f.read()
    except (IOError, OSError) as e:
        return f"Error reading log file: {str(e)}"
