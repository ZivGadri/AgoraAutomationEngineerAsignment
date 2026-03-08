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

from framework.drivers.driver_factory import DriverFactory

from framework.api.api_constants import APIUrl
from framework.api.clients.posts_client import PostsClient

# Load environment variables from .env once at collection time.
# This makes all variables available via os.getenv() / Config() throughout
# the entire test session.
load_dotenv()


# ---------------------------------------------------------------------------
# Config & API fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def posts_client() -> PostsClient:
    """Provides a configured PostsClient instance for the entire test session."""
    return PostsClient(base_url=APIUrl.API_BASE_URL)


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
    # Adjust path checks to handle both absolute paths and cross-platform slash differences
    has_ui_tests = any("tests" in str(item.fspath) and "ui" in str(item.fspath) for item in request.session.items)
    
    if not has_ui_tests:
        # If no UI tests are running (e.g., we ran 'pytest tests/api'), 
        # do not instantiate the webdriver.
        yield None
        return

    # Use the DriverFactory to instantiate and configure the WebDriver
    driver_instance = DriverFactory.get_chrome_driver()
    
    yield driver_instance
    
    # Teardown at the end of the entire test session
    if driver_instance:
        driver_instance.quit()


# ---------------------------------------------------------------------------
# Hooks
# ---------------------------------------------------------------------------

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
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


def pytest_sessionfinish():
    """
    Called after whole test run finished, right before returning the exit status to the system.
    Cleans up the local screenshots directory if run locally so it doesn't clutter the workspace over time.
    Keeps screenshots if running inside GitHub Actions.
    """
    import shutil
    
    # Clean up screenshots if not running in GitHub Actions
    if os.getenv("GITHUB_ACTIONS") != "true":
        screenshots_dir = os.path.join(os.getcwd(), "screenshots")
        if os.path.exists(screenshots_dir):
            try:
                shutil.rmtree(screenshots_dir)
                print(f"\n[Cleanup] Removed local screenshots directory: {screenshots_dir}")
            except Exception as e:
                print(f"\n[Cleanup Warning] Failed to clean up screenshots: {e}")
