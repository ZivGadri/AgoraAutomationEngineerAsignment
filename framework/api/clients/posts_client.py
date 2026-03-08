import requests
from framework.api.clients.base_client import BaseClient


class PostsClient(BaseClient):
    """
    API client for the /posts resource on JSONPlaceholder.
    Extends BaseClient with endpoint-specific methods for CRUD operations.
    """
    
    POSTS_ENDPOINT = "/posts"
    
    def create_post(self, title: str, body: str, user_id: int) -> requests.Response:
        """Sends a POST request to create a new post."""
        payload = {
            "title": title,
            "body": body,
            "userId": user_id
        }
        return self.post(self.POSTS_ENDPOINT, json=payload)
        
    def get_post(self, post_id: int) -> requests.Response:
        """Sends a GET request to retrieve a post by its ID."""
        return self.get(f"{self.POSTS_ENDPOINT}/{post_id}")
        
    def update_post(self, post_id: int, title: str, body: str, user_id: int) -> requests.Response:
        """Sends a PUT request for a full update of the post."""
        payload = {
            "title": title,
            "body": body,
            "userId": user_id
        }
        return self.put(f"{self.POSTS_ENDPOINT}/{post_id}", json=payload)
        
    def delete_post(self, post_id: int) -> requests.Response:
        """Sends a DELETE request to remove the post by its ID."""
        return self.delete(f"{self.POSTS_ENDPOINT}/{post_id}")
