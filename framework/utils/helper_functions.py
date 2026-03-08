"""
utils/helper_functions.py

Centralised configuration loader.
Reads all environment variables from the environment (or `.env` file via
python-dotenv in conftest.py) and exposes them as typed constants.

Provides safe fallback defaults using the constants module when appropriate.
"""
import datetime
import logging

import pytest
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


class TestMarkers:
    """
    Centralized registry of custom Pytest markers used across the framework.
    These markers provide enterprise-grade test management capabilities by allowing tests
    to be strictly linked to external test management systems and controlling test execution flow.
    
    Available Markers:
    - CASE_ID: Links the automation test method to its corresponding Test Case ID in an external
               Test Management Tool (e.g., TestRail `C1004`). 
               *Benefit*: Enables automated traceability and programmatic result reporting.
               
    - TEST_NAME: Provides a highly readable, human-friendly name for a test method.
                 *Benefit*: Vastly improves the clarity of test reports (like Allure or Slack bots)
                 instead of relying on raw Python method names like `test_checkout_flow`.
                 
    - DEPENDENCY: Controls execution flow by marking tests that depend on the successful execution
                  of a prior test (via `pytest-dependency`). 
                  *Benefit*: Prevents cascading failures. For example, if `test_create_post` fails, 
                  it's useless to run `test_update_post`. The framework will safely SKIP the dependent 
                  tests, keeping CI logs clean and reducing execution time.
                  
    - ORDER: Controls explicit execution order (from `pytest-order`).
    """
    CASE_ID = getattr(pytest.mark, "case_id")
    TEST_NAME = getattr(pytest.mark, "test_name")
    DEPENDENCY = getattr(pytest.mark, "dependency")
    ORDER = getattr(pytest.mark, "order")
