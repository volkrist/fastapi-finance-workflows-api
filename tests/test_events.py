def test_events_empty(client):
    r = client.get("/events")
    assert r.status_code == 200
    assert r.json() == []


def test_create_event_and_list(client):
    payload = {
        "event_type": "demo_event",
        "workflow_id": None,
        "step_id": None,
        "message": "hello",
        "payload": {"k": "v", "n": 1},
    }

    r = client.post("/events", json=payload)
    assert r.status_code == 201
    e = r.json()
    assert e["event_type"] == "demo_event"
    assert e["message"] == "hello"
    assert e["payload_json"] is not None

    r2 = client.get("/events?limit=50")
    assert r2.status_code == 200
    items = r2.json()
    assert len(items) == 1
    assert items[0]["id"] == e["id"]
