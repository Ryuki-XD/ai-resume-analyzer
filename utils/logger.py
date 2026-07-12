"""Logging configuration for the AI Resume Analyzer.

Provides a pre-configured logger with both console and rotating file
handlers. All modules should import ``get_logger`` and use it instead
of ``print`` for diagnostic output.
"""

import logging
import sys
from logging.handlers import RotatingFileHandler

from utils.constants import LOGS_DIR

# Ensure the logs directory exists
LOGS_DIR.mkdir(parents=True, exist_ok=True)

_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_LOG_FILE = LOGS_DIR / "app.log"
_MAX_BYTES = 5 * 1024 * 1024  # 5 MB
_BACKUP_COUNT = 3


def get_logger(name: str) -> logging.Logger:
    """Return a named logger with console + file handlers.

    Args:
        name: Logger name, typically ``__name__`` of the calling module.

    Returns:
        Configured ``logging.Logger`` instance.
    """
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers if called multiple times
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(_LOG_FORMAT)

    # Console handler (INFO and above)
    # Force UTF-8 on Windows to prevent UnicodeEncodeError with emoji
    try:
        import io
        utf8_stream = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        console_handler = logging.StreamHandler(utf8_stream)
    except AttributeError:
        console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Rotating file handler (DEBUG and above)
    file_handler = RotatingFileHandler(
        _LOG_FILE, maxBytes=_MAX_BYTES, backupCount=_BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
