# backend/tests/test_cazzate.py

def test_crea_cazzata(client, auth_headers, seed_data):
    response = client.post("/cazzate/", headers=auth_headers, json={
        "cazzaro_id": 1,
        "submitted_by": 2,
        "season_id": 1,
        "date": "2026-03-15",
        "month": 3,
        "description": "Ha dimenticato il portafoglio",
        "score": 5
    })
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "confirmed"
    assert data["score"] == 5

def test_score_fuori_range(client, auth_headers, seed_data):
    response = client.post("/cazzate/", headers=auth_headers, json={
        "cazzaro_id": 1,
        "submitted_by": 2,
        "season_id": 1,
        "date": "2026-03-15",
        "month": 3,
        "description": "Test",
        "score": 11    # fuori range — deve fallire
    })
    assert response.status_code == 422

def test_score_minimo(client, auth_headers, seed_data):
    response = client.post("/cazzate/", headers=auth_headers, json={
        "cazzaro_id": 1,
        "submitted_by": 2,
        "season_id": 1,
        "date": "2026-03-15",
        "month": 3,
        "description": "Test",
        "score": 0    # sotto il minimo — deve fallire
    })
    assert response.status_code == 422

def test_modifica_cazzata(client, auth_headers, seed_data):
    create = client.post("/cazzate/", headers=auth_headers, json={
        "cazzaro_id": 1,
        "submitted_by": 2,
        "season_id": 1,
        "date": "2026-03-15",
        "month": 3,
        "description": "Descrizione originale",
        "score": 5
    })
    cazzata_id = create.json()["id"]

    # Ora usa body JSON invece di query params
    update = client.patch(
        f"/cazzate/{cazzata_id}",
        headers=auth_headers,
        json={"score": 8}    # ← body JSON
    )
    assert update.status_code == 200
    assert update.json()["score"] == 8

def test_elimina_cazzata(client, auth_headers, seed_data):
    create = client.post("/cazzate/", headers=auth_headers, json={
        "cazzaro_id": 1,
        "submitted_by": 2,
        "season_id": 1,
        "date": "2026-03-15",
        "month": 3,
        "description": "Da eliminare",
        "score": 3
    })
    cazzata_id = create.json()["id"]

    delete = client.delete(f"/cazzate/{cazzata_id}", headers=auth_headers)
    assert delete.status_code == 200    # ← 200 con messaggio di conferma
    assert delete.json()["id"] == cazzata_id
    assert "eliminata" in delete.json()["message"].lower()

    # Verifica che non esista più
    get = client.get(f"/cazzate/{cazzata_id}", headers=auth_headers)
    assert get.status_code == 404