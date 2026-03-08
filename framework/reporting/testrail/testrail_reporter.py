"""
framework/reporting/testrail_reporter.py

Optional integration with the TestRail test management platform.
All TestRail API calls are guarded by the TESTRAIL_ENABLED flag in config.
When disabled, this module is a no-op and will not affect test results.

Responsibilities:
  - Authenticating with the TestRail API
  - Updating test run results after each test (pass / fail / skip)
  - Attaching failure messages and screenshots to TestRail cases
"""
