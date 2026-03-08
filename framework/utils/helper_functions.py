"""
utils/helper_functions.py

Centralised configuration loader.
Reads all environment variables from the environment (or `.env` file via
python-dotenv in conftest.py) and exposes them as typed constants.

Provides safe fallback defaults using the constants module when appropriate.
"""
import datetime
import logging
import pytz

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


class DateTime:
    """Helper class to configure and retrieve a datetime instance per class name."""

    @staticmethod
    def get_current_datetime() -> str:
        jerusalem_tz = pytz.timezone('Asia/Jerusalem')
        now_localized = datetime.datetime.now(jerusalem_tz)
        time_part = now_localized.strftime("%#d/%#m/%Y - %H:%M:%S")
        offset_str = now_localized.strftime('%z')
        formatted_offset = f"UTC{offset_str[:-2]}:{offset_str[-2:]}"
        final_output = f"{time_part} {formatted_offset}"

        return final_output
