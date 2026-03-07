"""
utils/constants.py

Project-wide constants, including default URLs, API endpoints, 
and explicit timeout/wait values.

Values here are static and not expected to change per environment.
Environment-specific variables (like credentials) live in config.py.
"""

class URLs:
    """Default base URLs for the project."""
    SAUCE_DEMO_BASE_URL: str = "https://www.saucedemo.com"
    API_BASE_URL: str = "https://jsonplaceholder.typicode.com"

class APIEndpoints:
    """Static API resource paths."""
    POSTS: str = "/posts"

class Timeouts:
    """Timeout settings in milliseconds (Playwright's default unit)."""
    DEFAULT_TIMEOUT_IN_SEC = 10.0
