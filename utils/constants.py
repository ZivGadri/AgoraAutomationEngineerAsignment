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
    """Timeout settings in seconds."""
    DEFAULT_TIMEOUT_IN_SEC = 10.0
    DEFAULT_SLEEP_IN_SEC = 0.7

class TestConstants:
    """Test related constants - """
    PRODUCTS_TO_ADD = [
        "Sauce Labs Backpack",
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Onesie"
    ]
    PRODUCT_TO_REMOVE = "Sauce Labs Bolt T-Shirt"
    TAX_PERCENTAGE = 8
    CHECKOUT_COMPLETE_SUCCESS_MSG = "Thank you for your order!"
