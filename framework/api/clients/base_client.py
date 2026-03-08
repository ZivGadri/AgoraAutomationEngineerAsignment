"""
api/base_client.py

Base HTTP client using the `requests` library.
"""

import logging
import requests
from typing import Optional, Dict


class BaseClient:
    """
    Base HTTP client designed to be extended by resource-specific clients.
    Manages a single `requests.Session` and provides safe, logged wrappers
    around common HTTP methods.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        # Ensure we always deal with JSON
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
        self.logger = logging.getLogger(self.__class__.__name__)

    def _log_request(self, method: str, url: str, **kwargs) -> None:
        """Hook to log outgoing requests. Future-proofs for allure reporting."""
        self.logger.info(f"Request: {method} {url}")
        if "json" in kwargs:
            self.logger.debug(f"Payload: {kwargs['json']}")

    def _log_response(self, response: requests.Response) -> None:
        """Hook to log incoming responses."""
        self.logger.info(f"Response: {response.status_code} {response.reason}")
        if response.text:
            self.logger.debug(f"Body: {response.text}")

    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        Unified request method that constructs the full URL, logs the transaction, 
        and executes the HTTP action, with added error handling to catch network failures.
        """
        url = f"{self.base_url}{endpoint}"
        self._log_request(method, url, **kwargs)
        
        try:
            response = self.session.request(method, url, **kwargs)
            self._log_response(response)
            return response
        except requests.exceptions.RequestException as e:
            self.logger.error(f"HTTP Request failed during {method} {url}: {e}")
            raise

    def get(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("PUT", endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("PATCH", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("DELETE", endpoint, **kwargs)

