# backend/tests/test_cazzate.py

def test_crea_cazzata(client, auth_headers, seed_data):
    response = client.post("/cazzate/", headers=auth_headers, json={
        "cazzaro_id": 1,
        "submitted_by": 2,
        "season_id": 1,
        "date": "2026-03-15",
        "month": 3,
        "description": "Ha dimenticato il portafoglio"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "pending"
    assert data["score"] is None

def test_conferma_cazzata(client, auth_headers, seed_data):
    # Prima crea
    create = client.post("/cazzate/", headers=auth_headers, json={
        "cazzaro_id": 1,
        "submitted_by": 2,
        "season_id": 1,
        "date": "2026-03-15",
        "month": 3,
        "description": "Test cazzata"
    })
    cazzata_id = create.json()["id"]

    # Poi conferma
    confirm = client.patch(
        f"/cazzate/{cazzata_id}/confirm",
        headers=auth_headers,
        json={"score": 7}
    )
    assert confirm.status_code == 200
    assert confirm.json()["score"] == 7
    assert confirm.json()["status"] == "confirmed"

def test_score_fuori_range(client, auth_headers, seed_data):
    create = client.post("/cazzate/", headers=auth_headers, json={
        "cazzaro_id": 1,
        "submitted_by": 2,
        "season_id": 1,
        "date": "2026-03-15",
        "month": 3,
        "description": "Test"
    })
    cazzata_id = create.json()["id"]

    # Score > 10 deve fallire
    confirm = client.patch(
        f"/cazzate/{cazzata_id}/confirm",
        headers=auth_headers,
        json={"score": 11}
    )
    assert confirm.status_code == 422

def test_doppia_conferma(client, auth_headers, seed_data):
    create = client.post("/cazzate/", headers=auth_headers, json={
        "cazzaro_id": 1,
        "submitted_by": 2,
        "season_id": 1,
        "date": "2026-03-15",
        "month": 3,
        "description": "Test"
    })
    cazzata_id = create.json()["id"]
    client.patch(f"/cazzate/{cazzata_id}/confirm",
                 headers=auth_headers, json={"score": 5})

    # Seconda conferma deve fallire
    second = client.patch(f"/cazzate/{cazzata_id}/confirm",
                          headers=auth_headers, json={"score": 8})
    assert second.status_code == 400