#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script logging_config.py
========================
Este script contém a configuração de logging para o projeto.
"""
import logging
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from config.settings import PROJECT_ROOT

DEFAULT_LOG_PATH = PROJECT_ROOT / "agentos_mcp_server.log"


def setup_logging(
    log_file: str | Path = DEFAULT_LOG_PATH,
    log_level: int = logging.INFO,
    log_dir: Path | None = None,
) -> None:
    """
    Configures the logging system.

    Args:
        log_file: Name of the log file (default: "agentos_mcp_server.log")
        log_level: Logging level (default: logging.INFO)
        log_dir: Directory to save logs. If None, saves in current directory.
    """
    # Determine log file path:
    if log_dir:
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / log_file
    else:
        log_path = Path(log_file)

    # Get root logger:
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove existing handlers to avoid duplicates:
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        handler.close()

    # Create formatters and handlers:
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # File handler:
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    # Console handler:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # Add handlers to root logger:
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured. Log file: {log_path.absolute()}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.

    Args:
        name: Name for the logger (usually __name__ of the module)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)
