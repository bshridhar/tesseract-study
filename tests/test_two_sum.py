from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_two_sum_success():
    resp = client.post("/api/two-sum", json={"nums": [2,7,11,15], "target": 9})
    assert resp.status_code == 200
    assert resp.json() == {"indices": [0,1]}

def test_two_sum_no_solution():
    resp = client.post("/api/two-sum", json={"nums": [1,2,3], "target": 7})
    assert resp.status_code == 404
    assert resp.json()["detail"] == "No two sum solution found"
