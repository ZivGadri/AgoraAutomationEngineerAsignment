"""
api/posts_client.py

API client for the /posts resource on JSONPlaceholder.
Extends BaseClient with endpoint-specific methods for CRUD operations.

Responsibilities:
  - create_post()  → POST /posts
  - get_post()     → GET  /posts/{id}
  - update_post()  → PUT  /posts/{id}
  - delete_post()  → DELETE /posts/{id}
"""
