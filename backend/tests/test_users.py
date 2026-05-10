# backend/tests/test_users.py

def test_get_users(client, auth_headers, seed_data):
    response = client.get("/users/", headers=auth_headers)
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 4
    nicknames = [u["nickname"] for u in users]
    assert "LUCA F" in nicknames
    assert "DAVIDE" in nicknames

def test_get_user_by_id(client, auth_headers, seed_data):
    response = client.get("/users/1", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_get_user_non_esistente(client, auth_headers, seed_data):
    response = client.get("/users/999", headers=auth_headers)
    assert response.status_code == 404