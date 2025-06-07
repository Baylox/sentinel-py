import logging
from logging.handlers import RotatingFileHandler
from typing import Optional, Dict, Any
from rich.console import Console
from rich.theme import Theme
from rich.logging import RichHandler

# Define SUCCESS level
SUCCESS = 25
logging.addLevelName(SUCCESS, "SUCCESS")

class ContextFilter(logging.Filter):
    """Filter to add context to log messages."""
    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, 'context'):
            record.context = 'GENERAL'
        return True

class CustomRichHandler(RichHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.console = Console(theme=Theme({
            "logging.level.success": "bold green",
            "logging.level.info": "bold cyan",
            "logging.level.warning": "bold yellow",
            "logging.level.error": "bold red",
            "logging.level.critical": "bold red reverse",
        }))

    def get_level_text(self, record: logging.LogRecord) -> str:
        if record.levelno == SUCCESS:
            return "[bold green]SUCCESS[/bold green]"
        return super().get_level_text(record)

def setup_advanced_logger(
    logfile: Optional[str] = None,
    max_bytes: int = 1_000_000,
    backup_count: int = 5
) -> logging.Logger:
    from pathlib import Path

    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    log_filename = logfile if logfile else "scanner.log"
    log_path = logs_dir / log_filename

    logger = logging.getLogger("sentinelpy")
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    context_filter = ContextFilter()
    logger.addFilter(context_filter)

    log_format = "%(asctime)s | [%(context)s] %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(log_format, date_format)

    console_handler = CustomRichHandler(
        show_time=True,
        show_path=False,
        rich_tracebacks=True,
        markup=True
    )
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    def success(self, msg: str, *args: Any, **kwargs: Any) -> None:
        if self.isEnabledFor(SUCCESS):
            self._log(SUCCESS, msg, args, **kwargs)

    logging.Logger.success = success

    return logger

def log_with_context(
    logger: logging.Logger,
    level: int,
    msg: str,
    *args: Any,
    context: str = "GENERAL",
    **kwargs: Any
) -> None:
    extra = kwargs.pop('extra', {})
    extra['context'] = context
    logger.log(level, msg, *args, extra=extra, **kwargs)
