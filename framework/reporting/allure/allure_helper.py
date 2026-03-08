"""
utils/allure_helper.py

Utility wrappers around the Allure reporting library.
Provides decorators and helpers to annotate test steps, attach
screenshots, logs, and other artefacts to the Allure report.

Responsibilities:
  - Exposing step(), attach(), and severity() helpers
  - Attaching browser screenshots on test failure
"""
