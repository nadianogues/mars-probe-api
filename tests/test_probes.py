def test_launch_probe_returns_initial_position(client):
    response = client.post("/probes", json={"x": 5, "y": 5, "direction": "NORTH"})
    assert response.status_code == 201
    data = response.json()
    assert data["x"] == 0
    assert data["y"] == 0
    assert data["direction"] == "NORTH"
    assert "id" in data


def test_launch_probe_returns_unique_ids(client):
    id_1 = client.post("/probes", json={"x": 5, "y": 5, "direction": "NORTH"}).json()["id"]
    id_2 = client.post("/probes", json={"x": 5, "y": 5, "direction": "NORTH"}).json()["id"]
    assert id_1 != id_2


def test_launch_probe_invalid_direction(client):
    response = client.post("/probes", json={"x": 5, "y": 5, "direction": "UP"})
    assert response.status_code == 422


def test_launch_probe_invalid_plateau_size(client):
    response = client.post("/probes", json={"x": 0, "y": 5, "direction": "NORTH"})
    assert response.status_code == 422
