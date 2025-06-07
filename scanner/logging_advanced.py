import logging
from logging.handlers import RotatingFileHandler
from typing import Optional, Dict, Any
import sys

# Define SUCCESS level
SUCCESS = 25
logging.addLevelName(SUCCESS, "SUCCESS")

class ContextFilter(logging.Filter):
    """Filter to add context to log messages."""
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Add context to log message."""
        if not hasattr(record, 'context'):
            record.context = 'GENERAL'
        return True

class RichLoggingHandler(logging.StreamHandler):
    """Logging handler with color support via rich."""
    
    def __init__(self, stream=None):
        super().__init__(stream or sys.stdout)
        try:
            from rich.logging import RichHandler
            self.rich_handler = RichHandler(
                show_time=True,
                show_path=False,
                rich_tracebacks=True
            )
        except ImportError:
            self.rich_handler = None
    
    def emit(self, record: logging.LogRecord) -> None:
        """Emit log message with colors if rich is available."""
        if self.rich_handler:
            self.rich_handler.emit(record)
        else:
            super().emit(record)

def setup_advanced_logger(
    logfile: Optional[str] = None,
    max_bytes: int = 1_000_000,
    backup_count: int = 5
) -> logging.Logger:
    """
    Configure an advanced logger with file rotation and colors.
    
    Args:
        logfile: Log file name
        max_bytes: Maximum log file size
        backup_count: Number of backup files to keep
    
    Returns:
        logging.Logger: Configured logger
    """
    from pathlib import Path
    
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Configure log file name
    log_filename = logfile if logfile else "scanner.log"
    log_path = logs_dir / log_filename
    
    # Create logger
    logger = logging.getLogger("sentinelpy")
    logger.setLevel(logging.DEBUG)
    
    # Avoid multiple handlers
    if logger.handlers:
        return logger
    
    # Add context filter
    context_filter = ContextFilter()
    logger.addFilter(context_filter)
    
    # Log format with context
    log_format = "[%(asctime)s] %(levelname)s - [%(context)s] %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(log_format, date_format)
    
    # Console handler with colors
    console_handler = RichLoggingHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    # Add success method
    def success(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a success message."""
        if self.isEnabledFor(SUCCESS):
            self._log(SUCCESS, msg, args, **kwargs)
    
    # Add success method to logger
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
    """
    Log a message with specific context.

    Args:
        logger: Logger to use
        level: Log level
        msg: Message to log
        *args: Additional arguments
        context: Message context (default: GENERAL)
        **kwargs: Additional keyword arguments
    """
    extra = kwargs.pop('extra', {})
    extra['context'] = context
    logger.log(level, msg, *args, extra=extra, **kwargs)