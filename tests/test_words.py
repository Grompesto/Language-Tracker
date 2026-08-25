def test_create_word_success(client, auth_header):
    response = client.post(
        "/words",
        json={
            "name": "Apple",
            "translation": "Яблоко",
            "difficulty": "Easy"
        },
        headers=auth_header
    )

    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Apple"
    assert data["translation"] == "Яблоко"
    assert data["ease_factor"] == 2.5
    assert "id" in data

def test_create_duplicate_word_fails(client, auth_header):
    client.post(
        "/words",
        json={
            "name": "Dog",
            "translation": "Собака",
            "difficulty": "Easy"
        },
        headers=auth_header
    )

    response = client.post(
        "/words",
        json={
            "name": "Dog",
            "translation": "Пёс",
            "difficulty": "Hard"
        },
        headers=auth_header
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Word already exists"


def test_create_word_without_auth_fails(client):
    response = client.post(
        "/words",
        json={
            "name": "Cat",
            "translation": "Кот",
            "difficulty": "Easy"
        }
    )

    assert response.status_code == 401

def test_get_all_words(client, auth_header):
    client.post(
        "/words",
        json={
            "name": "Banana",
            "translation": "Банан",
            "difficulty": "Easy"
        },
        headers=auth_header
    )

    response = client.get("/words", headers=auth_header)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    assert data[-1]["name"] == "Banana"

def test_delete_word_success(client, auth_header):
    create_response = client.post(
        "/words",
        json={
            "name": "Car",
            "translation": "Машина",
            "difficulty": "Easy"
        },
        headers=auth_header
    )
    word_id = create_response.json()["id"]

    delete_response = client.delete(f"/words/{word_id}", headers=auth_header)

    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Word deleted"}

    delete_again = client.delete(f"/words/{word_id}", headers=auth_header)
    assert delete_again.status_code == 404