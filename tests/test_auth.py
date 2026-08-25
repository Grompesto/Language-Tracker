def test_register_new_user_succeeds(client):
    response = client.post(
        "/words/register",
        json={"username": "alice", "password": "securepass123"},
    )
    assert response.status_code == 201
    assert response.json() == {"message": "User registered successfully"}

def test_register_duplicate_username_fails(client):
    client.post("/words/register", json={"username": "alice", "password": "securepass123"})

    response = client.post(
        "/words/register",
        json={"username": "alice", "password": "anotherpass456"}
    )
    assert response.status_code == 400

def test_login_with_correct_credentials_returns_token(registered_user, client):
    response = client.post(
        "/words/login",
        data={"username": registered_user["username"], "password": registered_user["password"]},
    )
    assert response.status_code == 200
    body = response.json()

    assert "access_token" in body
    assert isinstance(body["access_token"], str)
    assert body["token_type"] == "bearer"

def test_login_with_wrong_password_fails(registered_user,client):
    response = client.post(
        "/words/login",
        data={"username": registered_user["username"], "password": "wrongpassword"},
    )
    assert response.status_code == 401

def test_protected_endpoint_without_token_fails(client):
    response = client.get("/words")
    assert response.status_code == 401

def test_protected_endpoint_with_token_succeeds(client, auth_header):
    response = client.get("/words/me", headers=auth_header)
    assert response.status_code == 200
    assert response.json()["username"] == "tester"