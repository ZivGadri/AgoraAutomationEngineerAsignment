"""
tests/api/test_posts_crud.py

API tests for the /posts CRUD operations on JSONPlaceholder.

Test Cases:
  1. test_create_post  – POST /posts → 201, body matches, id is a positive int
  2. test_read_post    – GET  /posts/{id} → 200, valid JSON structure
  3. test_update_post  – PUT  /posts/{id} → 200, title updated, id unchanged
  4. test_delete_post  – DELETE /posts/{id} → 200
"""
