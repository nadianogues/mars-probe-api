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


# --- move probe ---


def test_move_probe_valid_sequence(client):
    probe_id = client.post("/probes", json={"x": 5, "y": 5, "direction": "NORTH"}).json()["id"]
    response = client.post(f"/probes/{probe_id}/commands", json={"commands": "MRM"})
    assert response.status_code == 200
    data = response.json()
    assert data["x"] == 1
    assert data["y"] == 1
    assert data["direction"] == "EAST"


def test_move_probe_out_of_bounds_does_not_move(client):
    probe_id = client.post("/probes", json={"x": 5, "y": 5, "direction": "SOUTH"}).json()["id"]
    response = client.post(f"/probes/{probe_id}/commands", json={"commands": "M"})
    assert response.status_code == 400
    # probe must remain at (0, 0)
    position = client.post(f"/probes/{probe_id}/commands", json={"commands": "L"}).json()
    assert position["x"] == 0
    assert position["y"] == 0


def test_move_probe_not_found(client):
    response = client.post("/probes/nonexistent/commands", json={"commands": "M"})
    assert response.status_code == 404


def test_move_probe_invalid_commands(client):
    probe_id = client.post("/probes", json={"x": 5, "y": 5, "direction": "NORTH"}).json()["id"]
    response = client.post(f"/probes/{probe_id}/commands", json={"commands": "MXM"})
    assert response.status_code == 422


def test_move_probe_multiple_sequences_accumulate(client):
    probe_id = client.post("/probes", json={"x": 5, "y": 5, "direction": "NORTH"}).json()["id"]
    client.post(f"/probes/{probe_id}/commands", json={"commands": "MM"})
    response = client.post(f"/probes/{probe_id}/commands", json={"commands": "MM"})
    data = response.json()
    assert data["x"] == 0
    assert data["y"] == 4
