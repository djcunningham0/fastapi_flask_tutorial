import pytest

from fastr.db.crud import get_user_by_username


def test_register(client, test_db, auth):
    """Register a new user and verify that they can log in"""
    assert client.get("/auth/register").status_code == 200
    response = client.post(
        "/auth/register", data={"username": "a", "password": "a"}, allow_redirects=True
    )
    assert response.url == f"{client.base_url}/auth/login"  # redirect to login page

    # make sure that user can log in
    test_login(client, auth, username="a", password="a")

    # make sure the user was added to the database
    assert get_user_by_username(test_db, username="a")


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("", "a", "username"),
        ("a", "", "password"),
    ),
)
def test_register_validate_input(client, username, password, message):
    """Validate that both username and password are required"""
    r = client.post("/auth/register", data={"username": username, "password": password})
    assert r.json() == {
        "detail": [
            {
                "loc": ["body", message],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ],
    }


def test_already_registered(client):
    """Validate that registration is rejected if the user already exists"""
    r = client.post(
        "/auth/register",
        data={"username": "test", "password": "test"},
        allow_redirects=True,
    )
    assert b"already registered" in r.content


@pytest.mark.parametrize(
    "username, password",
    [
        ("test", "test"),
        ("other", "passWord1"),
    ],
)
def test_login(client, auth, username, password):
    """Verify that existing users can log in"""
    assert client.get("/auth/login").status_code == 200
    response = auth.login(username, password)
    assert response.url == f"{client.base_url}/"  # redirects to /


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("a", "test", b"Incorrect username."),
        ("test", "a", b"Incorrect password."),
    ),
)
def test_login_validate_input(auth, username, password, message):
    """Verify that username and password must be correct"""
    response = auth.login(username, password)
    assert message in response.content


def test_logout(client, auth):
    """Verify that users can log out"""
    auth.login()

    with client:
        response = auth.logout()
        assert f'href="{client.base_url}/create">New</a>' not in response.text
