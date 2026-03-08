from framework.api.api_constants import APIEndpoints
from framework.api.clients.base_client import BaseClient
from framework.api.data_models.user_profile import UserProfileModel


class UserClient(BaseClient):

    def get_user_profile(self, post_id: int) -> UserProfileModel:
        """Sends a GET request to retrieve a post by its ID."""
        response = self.get(f"{APIEndpoints.USER_PROFILE}/{post_id}")
        return UserProfileModel.from_dict(response.json())

