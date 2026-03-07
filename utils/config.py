"""
utils/config.py

Centralised configuration loader.
Reads all environment variables from the environment (or `.env` file via
python-dotenv in conftest.py) and exposes them as typed constants.

Provides safe fallback defaults using the constants module when appropriate.
"""

import os
import logging
from dataclasses import dataclass

from utils.constants import URLs

class Logger:
    """Helper class to configure and retrieve a logger instance per class name."""
    
    @staticmethod
    def get_logger(class_name: str) -> logging.Logger:
        logger = logging.getLogger(class_name)
        # Prevent adding duplicate handlers if the logger already exists
        if not logger.hasHandlers():
            logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger


@dataclass(frozen=True)
class Config:
    """
    Project configuration loaded from environment variables.
    """

    # UI Configurations
    BASE_UI_URL: str = os.getenv("BASE_UI_URL", URLs.SAUCE_DEMO_BASE_URL)
    UI_USERNAME: str = os.getenv("UI_USERNAME", "standard_user")
    UI_PASSWORD: str = os.getenv("UI_PASSWORD", "secret_sauce")

    # API Configurations
    BASE_API_URL: str = os.getenv("BASE_API_URL", URLs.API_BASE_URL)

    # Feature Flags
    TESTRAIL_ENABLED: bool = os.getenv("TESTRAIL_ENABLED", "false").lower() == "true"
