# backend/tests/test_auth.py

def test_login_corretto(client):
    response = client.post("/auth/login", json={"password": "pesciolinoduro7"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_password_errata(client):
    response = client.post("/auth/login", json={"password": "sbagliata"})
    assert response.status_code == 401

# tests/test_auth.py
def test_endpoint_protetto_senza_token(client):
    response = client.get("/users/")
    assert response.status_code == 401  # 401 è corretto con HTTPBearer

def test_endpoint_protetto_con_token(client, auth_headers, seed_data):
    response = client.get("/users/", headers=auth_headers)
    assert response.status_code == 200