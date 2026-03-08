"""
tests/api/test_posts.py

API tests for the /posts endpoint. 

The test cases follow the JSONPlaceholder CRUD assignment:
1. Create a Post (POST)
2. Read the Post (GET)
3. Update the Post (PATCH)
4. Delete the Post (DELETE)

Note: Tests are run sequentially, sharing the created `post_id` through a fixture cache
or test context because they operate on the single entity created in Step 1.
"""

import pytest
import pytest_check as check

# Test context to store values (like the created post ID) across the sequential tests
class TestContext:
    post_id = None

@pytest.fixture(scope="module")
def context():
    return TestContext()

def test_create_post(posts_client, context):
    """
    Step 1: Create a Post
    Sends a POST request.
    Verifies:
      - Status code 201
      - Body contains correct title, body, userId
      - Response contains a positive integer ID (saved for next steps)
    """
    expected_title = "Candidate Post"
    expected_body = "Hello from automation"
    expected_user_id = 1
    
    response = posts_client.create_post(
        title=expected_title,
        body=expected_body,
        user_id=expected_user_id
    )
    
    check.equal(response.status_code, 201, f"Expected 201 Created, got {response.status_code}")
    
    response_json = response.json()
    
    # Assert payload details match
    check.equal(response_json.get("title"), expected_title, f"Expected title {expected_title}, got {response_json.get('title')}")
    check.equal(response_json.get("body"), expected_body, f"Expected body {expected_body}, got {response_json.get('body')}")
    check.equal(response_json.get("userId"), expected_user_id, f"Expected userId {expected_user_id}, got {response_json.get('userId')}")
    
    # Assert ID exists and is a positive integer
    post_id = response_json.get("id")
    check.is_true(isinstance(post_id, int), f"Expected 'id' to be an integer, got {type(post_id)}")
    check.is_true(post_id > 0, "Expected 'id' to be a positive integer")
    
    # Save ID in context for subsequent CRUD steps
    context.post_id = post_id


def test_get_post(posts_client, context):
    """
    Step 2: Read the Post
    Sends a GET request for the previously created post.
    Verifies:
      - Status code 200
      - ID matches the saved ID
      - Returned JSON structure is valid (contains id, title, body, userId)
    """
    post_id = context.post_id
    check.is_true(post_id is not None, "Post ID missing. Did `test_create_post` run and succeed?")
    
    response = posts_client.get_post(post_id)
    
    # Verify status code
    check.is_true(response.status_code == 200, f"Expected 200 OK, got {response.status_code}")
    
    response_json = response.json()
    
    # Verify ID matches
    check.equal(response_json.get("id"), post_id, f"Expected id {post_id}, got {response_json.get('id')}")
    
    # Verify JSON structure contains expected keys
    expected_keys = {"id", "title", "body", "userId"}
    actual_keys = set(response_json.keys())
    check.is_true(expected_keys.issubset(actual_keys), f"Response JSON missing required keys. Found: {actual_keys}")


def test_update_post(posts_client, context):
    """
    Step 3: Update the Post
    Sends a PUT request to fully update the post.
    Verifies:
      - Status code 200
      - Response contains the updated title
      - ID remains the same
    """
    post_id = context.post_id
    new_title = "Candidate Post - Updated Edition"
    original_body = "Hello from automation"
    original_user_id = 1
    
    response = posts_client.update_post(post_id, new_title, original_body, original_user_id)
    
    # Verify status
    check.equal(response.status_code, 200, f"Expected 200 OK, got {response.status_code}")
    
    response_json = response.json()
    
    # Verify title was updated
    check.equal(response_json.get("title"), new_title, f"Expected title '{new_title}', got '{response_json.get('title')}'")
    
    # Verify ID remained the same
    check.equal(response_json.get("id"), post_id, f"Expected id '{post_id}', got '{response_json.get('id')}'")


def test_delete_post(posts_client, context):
    """
    Step 4: Delete the Post
    Sends a DELETE request for the stored post.
    Verifies:
      - Status code 200
    """
    post_id = context.post_id
    
    response = posts_client.delete_post(post_id)
    
    # JSONPlaceholder typically returns an empty object {} and a 200 OK on DELETE
    check.equal(response.status_code, 200, f"Expected 200 OK, got {response.status_code}")
