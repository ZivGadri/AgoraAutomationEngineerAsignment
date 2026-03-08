import os

from framework.reporting.testrail.testrail_constants import EnvVars, TestRailAttributes
from framework.utils.helper_functions import Logger
from testrail_api import TestRailAPI


class TestRailClient:
    def __init__(self):
        self.logger = Logger.get_logger("TestRailClient")
        self.url = TestRailAttributes.TESTRAIL_URL
        self.username = EnvVars.TESTRAIL_USERNAME
        self.key = EnvVars.TESTRAIL_KEY
        self.is_connected = False
        self.client = None

        try:
            if not all([self.url, self.username, self.key]):
                raise ValueError(
                    "TestRail credentials (URL, USERNAME, KEY) could not be found in environment variables")
            self.client = TestRailAPI(self.url, self.username, self.key)
            self.is_connected = True
        except ValueError as e:
            self.logger.warning(f"TestRail integration disabled. {e}")
            os.environ["REPORT_TO_TESTRAIL"] = "False"  # Ensure flag is off
        except Exception as e:
            self.logger.warning(f"TestRail client initialization failed: {e}")
            os.environ["REPORT_TO_TESTRAIL"] = "False"  # Ensure flag is off

    def _check_connection(self):
        if not self.is_connected or self.client is None:
            self.logger.error("TestRail client is not connected. API call aborted.")
            return False
        return True

    def get_project_id_by_name(self, project_name: str) -> int | None:
        if not self._check_connection(): return None
        try:
            projects_response = self.client.projects.get_projects()  # Corrected method call: get_all() -> get_projects()
            if projects_response and 'projects' in projects_response:
                for project in projects_response.get('projects', []):
                    if project.get('name') == project_name:
                        return project.get('id')
            self.logger.error(f"Project '{project_name}' not found in TestRail or API call failed.")
            return None
        except Exception as e:
            self.logger.error(f"TestRail API call (get_projects) failed: {e}")
            return None

    def get_suite_id_by_name(self, project_id: int, suite_name: str) -> int | None:
        if not self._check_connection(): return None
        try:
            suites_response = self.client.suites.get_suites(project_id)
            if suites_response and 'suites' in suites_response:
                for suite in suites_response.get('suites', []):
                    if suite.get('name') == suite_name:
                        return suite.get('id')
            self.logger.error(f"Suite '{suite_name}' not found in project {project_id} or API call failed.")
            return None
        except Exception as e:
            self.logger.error(f"TestRail API call (get_suites) failed for project {project_id}: {e}")
            return None

    def get_all_test_cases_for_project(self, project_id: int) -> list | None:
        if not self._check_connection(): return None
        all_cases = []
        try:
            suites_response = self.client.suites.get_suites(project_id)
            if not suites_response or 'suites' not in suites_response: return None

            for suite in suites_response.get('suites', []):
                suite_id = suite.get('id')
                if suite_id:
                    # TestRail API get_cases returns a list of cases for a given project and suite.
                    # We filter by `custom_automation_status=1` (assuming 1 is 'Automated') later in manager.
                    # No direct filter for automation status in get_cases parameters as per testrail-api docs.
                    cases_response = self.client.cases.get_cases(project_id, suite_id=suite_id)
                    if cases_response and 'cases' in cases_response:
                        for case in cases_response.get('cases', []):
                            case['suite_id'] = suite_id  # Add suite_id to case for later grouping
                            all_cases.append(case)
            return all_cases
        except Exception as e:
            self.logger.error(f"TestRail API call (get_cases) failed for project {project_id}: {e}")
            return None

    def get_all_test_cases_from_test_suites(self, project_id: int, test_suites_ids: list) -> list | None:
        global test_suite_id
        if not self._check_connection(): return None
        all_cases = []
        try:
            for test_suite_id in test_suites_ids:
                tset_suite_cases = self.client.cases.get_suite_cases(project_id, suite_id=test_suite_id)
                all_cases.extend(tset_suite_cases)
        except Exception as e:
            self.logger.error(f"TestRail API call (get_suite_cases) failed for test suite id {test_suite_id}: {e}")
        return all_cases

    def create_test_plan(self, project_id: int, name: str, description: str = None) -> dict | None:
        if not self._check_connection(): return None
        data = {'name': name, 'description': description}
        try:
            plan = self.client.plans.add_plan(project_id, **data)
            if not plan: self.logger.error(f"Failed to create test plan '{name}'.")
            return plan
        except Exception as e:
            self.logger.error(f"TestRail API call (add_plan) failed: {e}")
            return None

    def add_test_run_to_plan(self, plan_id: int, suite_id: int, name: str, case_ids: list,
                             assignedto_id: int = None) -> dict | None:
        if not self._check_connection(): return None
        # Add an entry to an existing plan
        data = {
            'name': name,
            'case_ids': case_ids,
            'include_all': False,  # Only include specified cases
        }
        if assignedto_id is not None:  # Only add if provided
            data['assignedto_id'] = assignedto_id

        try:
            # project_id is no longer passed as a direct argument to add_plan_entry in testrail_api
            plan_entry = self.client.plans.add_plan_entry(plan_id, suite_id, **data)
            if not plan_entry: self.logger.error(
                f"Failed to add test run entry for suite {suite_id} to plan {plan_id}.")
            return plan_entry
        except Exception as e:
            self.logger.error(f"TestRail API call (add_plan_entry) failed: {e}")
            return None

    def add_result_for_case(self, run_id: int, case_id: int, status_id: int, comment: str = None) -> dict | None:
        if not self._check_connection(): return None
        data = {'status_id': status_id, 'comment': comment}
        try:
            result = self.client.results.add_result_for_case(run_id, case_id, **data)
            if not result: self.logger.error(f"Failed to add result for case C{case_id} in run {run_id}.")
            return result
        except Exception as e:
            self.logger.error(f"TestRail API call (add_result_for_case) failed: {e}")
            return None

    def update_plan(self, plan_id: int, description: str = None, name: str = None) -> dict | None:
        """Updates a test plan with a new description or name."""
        if not self._check_connection(): return None
        data = {}
        if description is not None:
            data['description'] = description
        if name is not None:
            data['name'] = name

        if not data:
            self.logger.warning(f"No data provided to update plan {plan_id}.")
            return None

        try:
            updated_plan = self.client.plans.update_plan(plan_id, **data)
            if not updated_plan: self.logger.error(f"Failed to update test plan {plan_id}.")
            return updated_plan
        except Exception as e:
            self.logger.error(f"TestRail API call (update_plan) failed: {e}")
            return None

    def close_test_plan(self, plan_id: int) -> dict | None:
        if not self._check_connection(): return None
        data = {'is_completed': True}
        try:
            closed_plan = self.client.plans.update_plan(plan_id, **data)  # Using update_plan to set is_completed
            if not closed_plan: self.logger.error(f"Failed to close test plan {plan_id}.")
            return closed_plan
        except Exception as e:
            self.logger.error(f"TestRail API call (update_plan to close) failed: {e}")
            return None

    def update_run(self, run_id: int, description: str = None, name: str = None) -> dict | None:
        """Updates a test run with a new description or name."""
        if not self._check_connection(): return None
        data = {}
        if description is not None:
            data['description'] = description
        if name is not None:
            data['name'] = name

        if not data:
            self.logger.warning(f"No data provided to update run {run_id}.")
            return None

        try:
            updated_run = self.client.runs.update_run(run_id, **data)
            if not updated_run: self.logger.error(f"Failed to update test run {run_id}.")
            return updated_run
        except Exception as e:
            self.logger.error(f"TestRail API call (update_run) failed: {e}")
            return None

    def update_plan_entry(self, plan_id: int, entry_id: str, description: str = None, name: str = None) -> dict | None:
        """Updates a plan entry (which contains runs) with a new description or name."""
        if not self._check_connection(): return None
        data = {}
        if description is not None:
            data['description'] = description
        if name is not None:
            data['name'] = name

        if not data:
            self.logger.warning(f"No data provided to update plan entry {entry_id}.")
            return None

        try:
            updated_entry = self.client.plans.update_plan_entry(plan_id, entry_id, **data)
            if not updated_entry: self.logger.error(f"Failed to update plan entry {entry_id}.")
            return updated_entry
        except Exception as e:
            self.logger.error(f"TestRail API call (update_plan_entry) failed: {e}")
            return None

    def get_testrail_status_id(self, status: str) -> int | None:
        """Helper to get status ID from TestRail (e.g., 'Passed' -> 1)."""
        # This would typically require fetching all statuses via get_statuses,
        # but for simplicity, we'll use hardcoded common ones as per TestRail API docs.
        status_map = {
            'passed': 1,
            'blocked': 2,
            'untested': 3,
            'retest': 4,
            'failed': 5
        }
        return status_map.get(status.lower())

    def add_attachment_to_result(self, result_id: int, attachment_path: str) -> dict | None:
        if not self._check_connection(): return None
        if not os.path.exists(attachment_path):
            self.logger.warning(f"Attachment file not found: {attachment_path}")
            return None

        try:
            # testrail_api usually supports add_attachment_to_result(result_id, path)
            response = self.client.attachments.add_attachment_to_result(result_id, attachment_path)
            if not response:
                self.logger.error(f"Failed to add attachment {attachment_path} to result {result_id}.")
            return response
        except Exception as e:
            self.logger.error(f"TestRail API call (add_attachment_to_result) failed: {e}")
            return None