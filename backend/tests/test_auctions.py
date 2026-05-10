# backend/tests/test_auctions.py

def test_crea_auction(client, auth_headers, seed_data):
    response = client.post("/auctions/", headers=auth_headers, json={
        "season_id": 1,
        "player_id": 1,
        "cazzaro_id": 2,
        "month": 3,
        "cost": 45
    })
    assert response.status_code == 201
    assert response.json()["cost"] == 45

def test_player_non_compra_se_stesso(client, auth_headers, seed_data):
    """Player 1 ha user_id=1, Cazzaro 1 ha user_id=1 — deve fallire."""
    response = client.post("/auctions/", headers=auth_headers, json={
        "season_id": 1,
        "player_id": 1,
        "cazzaro_id": 1,
        "month": 3,
        "cost": 50
    })
    assert response.status_code == 400

def test_player_un_solo_acquisto_per_mese(client, auth_headers, seed_data):
    client.post("/auctions/", headers=auth_headers, json={
        "season_id": 1,
        "player_id": 1,
        "cazzaro_id": 2,
        "month": 3,
        "cost": 45
    })
    # Stesso player, stesso mese — deve fallire
    second = client.post("/auctions/", headers=auth_headers, json={
        "season_id": 1,
        "player_id": 1,
        "cazzaro_id": 3,
        "month": 3,
        "cost": 30
    })
    assert second.status_code == 400