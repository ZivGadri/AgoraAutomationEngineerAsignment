"""
conftest.py

Root-level Pytest configuration file.

All fixtures and hooks defined here are automatically available to every test
in the project without any explicit import.

Fixture overview
----------------
  config        (session) – Loads .env and exposes typed config constants.
  posts_client  (session) – Ready-to-use PostsClient for API tests.

Hook overview
-------------
  pytest_runtest_makereport – Captures a full-page screenshot on UI test
                              failure and saves it to the `screenshots/`
                              directory for post-mortem debugging.
"""

import pytest
from dotenv import load_dotenv

from api.posts_client import PostsClient
from utils.config import Config

# Load environment variables from .env once at collection time.
# This makes all variables available via os.getenv() / Config() throughout
# the entire test session.
load_dotenv()


# ---------------------------------------------------------------------------
# Hooks
# ---------------------------------------------------------------------------

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook that runs after every phase of a test (setup / call / teardown).

    On test failure during the 'call' phase this hook:
      1. Checks whether a Playwright `page` fixture was active for this test.
      2. If so, takes a full-page screenshot and saves it under screenshots/.

    The `tryfirst=True` + `hookwrapper=True` combination ensures this hook runs
    before the default report handling, so the screenshot is captured while the
    browser is still open.

    Args:
        item (pytest.Item): The test item currently being executed.
        call (pytest.CallInfo): Information about the test phase.
    """
    outcome = yield  # let the test run; capture its outcome
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            screenshot_path = f"screenshots/{item.name}.png"
            page.screenshot(path=screenshot_path, full_page=True)


# ---------------------------------------------------------------------------
# Config fixture
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def config() -> Config:
    """
    Loads and returns the application configuration for the entire test session.

    Session-scoped so the .env file is read only once, and the same Config
    object is reused across all tests — avoiding repeated I/O and ensuring
    every test sees identical configuration.

    Returns:
        Config: Typed configuration object exposing BASE_UI_URL, BASE_API_URL,
                credentials, and feature flags loaded from the .env file.
    """
    return Config()


# ---------------------------------------------------------------------------
# API fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def posts_client(config: Config) -> PostsClient:
    """
    Provides a configured PostsClient instance for the entire test session.

    Session-scoped because the HTTP client is stateless — there is no browser
    session or shared mutable state between API tests, so it is safe and
    efficient to share a single instance.

    Args:
        config (Config): The session-scoped config fixture; supplies BASE_API_URL.

    Returns:
        PostsClient: Initialised client ready to call all /posts endpoints.
    """
    return PostsClient(base_url=config.BASE_API_URL)


# ---------------------------------------------------------------------------
# Browser context customisation (UI fixtures)
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    """
    Extends pytest-playwright's default BrowserContext arguments.

    Merges our project-level overrides (viewport, locale, etc.) with whatever
    pytest-playwright already provides, so existing CLI flags like
    --headed or --slowmo still work as expected.

    Args:
        browser_context_args (dict): Default context args from pytest-playwright.

    Returns:
        dict: Merged context arguments applied to every test's browser context.
    """
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "locale": "en-US",
    }
