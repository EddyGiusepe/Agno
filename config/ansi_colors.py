#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script ansi_colors.py
=====================
Este script contém códigos ANSI para formatação de cores no terminal.
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from config.logging_config import (
    get_logger,
    setup_logging,
)

setup_logging()
logger = get_logger(__name__)

# ANSI codes for colors:
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"


if __name__ == "__main__":
    logger.info(f"{RED}Hello, World!{RESET}")
