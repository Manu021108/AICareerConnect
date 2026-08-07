"""Tests for authentication routes."""


def test_register_page_loads(client):
    response = client.get("/auth/register")
    assert response.status_code == 200


def test_login_page_loads(client):
    response = client.get("/auth/login")
    assert response.status_code == 200


def test_register_and_login(client, db):
    # Register
    client.post("/auth/register", data={
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepass123",
    })

    # Login
    response = client.post("/auth/login", data={
        "email": "test@example.com",
        "password": "securepass123",
    }, follow_redirects=True)

    assert response.status_code == 200
