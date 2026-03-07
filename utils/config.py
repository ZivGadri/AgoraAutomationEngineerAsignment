"""
utils/config.py

Centralised configuration loader.
Reads all environment variables from the `.env` file at startup and
exposes them as typed constants for use across the framework.

Responsibilities:
  - Loading `.env` via python-dotenv
  - Validating that required variables are present
  - Exposing typed config values (URLs, credentials, feature flags)
"""
