def test_hello(client):
    response = client.get("/hello")
    assert response.content == b"Hello, World!"
