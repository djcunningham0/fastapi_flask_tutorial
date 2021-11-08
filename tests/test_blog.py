import pytest

from fastr.db.crud import get_post_by_id


def test_index(client, auth):
    """Test that the appropriate fields appear on / before and after login"""
    response = client.get("/")
    assert "Log In" in response.text
    assert "Register" in response.text
    assert f'href="{client.base_url}/create">New</a>' not in response.text

    auth.login()
    response = client.get("/")
    assert f'href="{client.base_url}/create">New</a>' in response.text
    assert "Log Out" in response.text
    assert "test title" in response.text
    assert "by test on 2018-01-01" in response.text
    assert "test\nbody" in response.text
    print(response.text)
    assert f'href="{client.base_url}/1/update"' in response.text


@pytest.mark.parametrize(
    "path",
    (
        "/create",
        "/1/update",
        "/1/delete",
    ),
)
def test_login_required(client, path):
    """Verify that requests are redirected to login screen when no use is logged in"""
    response = client.post(path, allow_redirects=True)
    assert response.url == f"{client.base_url}/auth/login"


def test_author_required(test_db, client, auth):
    """Users can only update or delete posts that they authored"""
    auth.login()

    # current user can't update or delete another user's post
    update_r = client.post("/2/update", data={"title": "new", "body": "update"})
    assert update_r.status_code == 403
    assert client.post("/2/delete").status_code == 403

    # current user doesn't see edit link
    print(client.get("/").text)
    assert f'href="{client.base_url}/2/update"' not in client.get("/").text


@pytest.mark.parametrize(
    "path, data",
    [
        ("/3/update", {"title": "new", "body": "update"}),
        ("/3/delete", None),
    ],
)
def test_exists_required(client, auth, path, data):
    """Return a 404 error if the post ID does not exist"""
    auth.login()
    r = client.post(path, data=data)
    assert r.status_code == 404


def test_create(client, auth, test_db):
    """Validate that a logged in user can create a post"""
    auth.login()
    assert client.get("/create").status_code == 200
    client.post("/create", data={"title": "created title", "body": "created body"})

    # confirm that the new post has been created with an auto incremented id
    post = get_post_by_id(test_db, id=3)
    assert post
    assert post.author.username == "test"

    # confirm there are now 3 posts in the database
    query_result = test_db.execute("SELECT COUNT(id) as cnt FROM post")
    cnt = [r["cnt"] for r in query_result][0]
    assert cnt == 3


def test_update(client, auth, test_db):
    """Validate that a logged in user can update a post that they authored"""
    auth.login()
    assert client.get("/1/update").status_code == 200
    client.post("/1/update", data={"title": "updated", "body": "new body"})

    # confirm that the update is reflected in the database
    post = get_post_by_id(test_db, id=1)
    assert post.title == "updated"
    assert post.body == "new body"
    assert post.author.username == "test"


@pytest.mark.parametrize(
    "path",
    (
        "/create",
        "/1/update",
    ),
)
def test_create_update_validate(client, auth, path):
    """Validate that title is required when creating or updating a post"""
    auth.login()
    response = client.post(path, data={"title": "", "body": ""})
    print(response.json())
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "title"],
                "msg": "field required",
                "type": "value_error.missing",
            },
        ]
    }


def test_delete(client, auth, test_db):
    """Validate that a user can delete a post that they authored"""
    auth.login()
    response = client.post("/1/delete", allow_redirects=True)
    assert response.url == f"{client.base_url}/"

    # confirm it was deleted from the database
    post = get_post_by_id(test_db, id=1)
    assert post is None
