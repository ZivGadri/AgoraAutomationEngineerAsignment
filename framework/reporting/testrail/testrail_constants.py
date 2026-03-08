import os


class EnvVars:
    # Feature Flags
    TESTRAIL_ENABLED: bool = os.getenv("TESTRAIL_ENABLED", "false").lower() == "true"
    TESTRAIL_USERNAME = os.getenv("TESTRAIL_USERNAME")
    TESTRAIL_KEY = os.getenv("TESTRAIL_KEY")

class TestRailAttributes:
    # TestRail Credentials
    TESTRAIL_URL = "https://something.testrail.io/"

    # Global TestRail configuration for manager
    TESTRAIL_PROJECT_NAME = "Agora RE"
    TR_AUTOMATION_ASSIGNED_TO_ID = 3 # Assigning all test runs to automation user in TestRail