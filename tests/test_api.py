from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_validate_ok():
    r = client.post(
        "/transactions/validate",
        json={"product_line": "Food", "unit_price": 10, "quantity": 2, "kind": "discounted", "rate": 0.1},
    )
    assert r.status_code == 200
    assert r.json()["total"] == 18.0


def test_validate_rejects_bad_price():
    r = client.post(
        "/transactions/validate",
        json={"product_line": "Food", "unit_price": -5, "quantity": 2},
    )
    assert r.status_code == 422