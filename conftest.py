"""
conftest.py

Root-level Pytest configuration file.

All fixtures and hooks defined here are automatically available to every test
in the project without any explicit import.

Fixture overview
----------------
  config        (session) – Loads .env and exposes typed config constants.
  posts_client  (session) – Ready-to-use PostsClient for API tests.
  driver        (session) – Selenium WebDriver instance for UI tests.

Hook overview
-------------
  pytest_runtest_makereport – Captures a full-page screenshot on UI test
                              failure and saves it to the `screenshots/`
                              directory for post-mortem debugging.
"""

import os
import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from api.posts_client import PostsClient
from utils.config import Config

# Load environment variables from .env once at collection time.
# This makes all variables available via os.getenv() / Config() throughout
# the entire test session.
load_dotenv()


# ---------------------------------------------------------------------------
# Config & API fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def config() -> Config:
    """Loads and returns the application configuration for the entire test session."""
    return Config()


@pytest.fixture(scope="session")
def posts_client(config: Config) -> PostsClient:
    """Provides a configured PostsClient instance for the entire test session."""
    return PostsClient(base_url=config.BASE_API_URL)


# ---------------------------------------------------------------------------
# UI context & Webdriver setup
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def driver(request):
    """
    Instantiates the Selenium WebDriver at the beginning of the test session,
    but ONLY if tests from the 'tests/ui' directory have been collected for this run.

    Yields the driver for the UI tests to use, then quits it cleanly at 
    the end of the session.
    """
    # Check if there are any UI tests in the current pytest session
    has_ui_tests = any("tests/ui" in str(item.fspath) for item in request.session.items)
    
    if not has_ui_tests:
        # If no UI tests are running (e.g., we ran 'pytest tests/api'), 
        # do not instantiate the webdriver.
        yield None
        return

    # Use Webdriver Manager (by Boni Garcia) to automatically download 
    # the correct ChromeDriver binary for the local machine's Chrome version.
    service = ChromeService(ChromeDriverManager().install())
    
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # Uncomment for headless execution in CI:
    # options.add_argument("--headless")
    
    driver_instance = webdriver.Chrome(service=service, options=options)
    
    # Implicit wait as a fallback, though explicit waits in BasePage are preferred.
    driver_instance.implicitly_wait(5)
    
    yield driver_instance
    
    # Teardown at the end of the entire test session
    driver_instance.quit()


# ---------------------------------------------------------------------------
# Hooks
# ---------------------------------------------------------------------------

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook that runs after every phase of a test (setup / call / teardown).
    Takes a screenshot on failure if the test was using the `driver` fixture.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Check if this specific test requested the Selenium driver
        if "driver" in item.fixturenames:
            driver_instance = item.funcargs.get("driver")
            if driver_instance:
                os.makedirs("screenshots", exist_ok=True)
                screenshot_path = os.path.join("screenshots", f"{item.name}.png")
                driver_instance.save_screenshot(screenshot_path)
