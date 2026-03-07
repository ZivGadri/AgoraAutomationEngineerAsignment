"""
api/base_client.py

Base HTTP client using the `requests` library.
All API-specific clients inherit from this class to share session
management, default headers, logging, and error handling.

Responsibilities:
  - Initialising the requests.Session with base URL and headers
  - Logging all outgoing requests and incoming responses
  - Providing generic GET, POST, PUT, PATCH, DELETE wrappers
  - Raising consistent exceptions on unexpected status codes
"""
