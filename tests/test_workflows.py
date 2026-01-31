def test_list_workflows_empty(client):
    r = client.get("/workflows")
    assert r.status_code == 200
    assert r.json() == []


def test_create_workflow_and_get(client):
    payload = {
        "name": "Demo workflow",
        "description": "Test workflow",
        "steps": [{"title": "Step one"}, {"title": "Step two"}],
    }

    r = client.post("/workflows", json=payload)
    assert r.status_code == 201
    data = r.json()

    assert "id" in data
    assert data["name"] == "Demo workflow"
    assert len(data["steps"]) == 2
    assert data["steps"][0]["status"] == "pending"

    workflow_id = data["id"]

    r2 = client.get(f"/workflows/{workflow_id}")
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2["id"] == workflow_id
    assert len(data2["steps"]) == 2


def test_get_workflow_404(client):
    r = client.get("/workflows/999999")
    assert r.status_code == 404


def test_complete_step(client):
    payload = {
        "name": "Complete test",
        "description": None,
        "steps": [{"title": "A"}, {"title": "B"}],
    }
    created = client.post("/workflows", json=payload).json()
    wid = created["id"]
    step_id = created["steps"][0]["id"]

    r = client.post(f"/workflows/{wid}/steps/{step_id}/complete")
    assert r.status_code == 200
    out = r.json()
    assert out["workflow_id"] == wid
    assert out["step_id"] == step_id
    assert out["status"] == "completed"

    # шаг реально стал completed
    after = client.get(f"/workflows/{wid}").json()
    step = [s for s in after["steps"] if s["id"] == step_id][0]
    assert step["status"] == "completed"
    assert step["completed_at"] is not None


def test_complete_step_404(client):
    # нет такого шага / workflow
    r = client.post("/workflows/1/steps/1/complete")
    assert r.status_code == 404
