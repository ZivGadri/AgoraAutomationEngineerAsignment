"""
framework/api/api_constants.py

API related constants and env vars, including default URLs, API endpoints, and more.
Values here are static and not expected to change on runtime.
"""

class APIUrl:
    """URLs for the project."""
    API_BASE_URL: str = "https://jsonplaceholder.typicode.com"

class APIEndpoints:
    """API endpoints for the project."""
    POSTS: str = "/posts"
    USER_PROFILE: str = "/user/profile"

class APITestConstants:
    """API test constants for the project."""
    RETRY_ATTEMPTS: int = 10
    INTERVAL_SECONDS: int = 5
