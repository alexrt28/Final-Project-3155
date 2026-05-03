from fastapi.testclient import TestClient
from ..controllers import orders as controller
from ..main import app
import pytest
from ..models import orders as model
from datetime import datetime, timedelta

client = TestClient(app)

def test_create_promo_code():
    response = client.post("/promo-codes/", json={
        "code": "SAVE10",
        "discount": 10,
        "discount_type": "percent",
        "expiry": (datetime.now() + timedelta(days=7)).isoformat()
    })
    assert response.status_code == 200
    assert response.json()["code"] == "SAVE10"

def test_read_all_promo_codes():
    response = client.get("/promo-codes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_promo_code():
    create = client.post("/promo-codes/", json={
        "code": "SPRING15",
        "discount": 15,
        "discount_type": "percent",
        "expiry": (datetime.now() + timedelta(days=30)).isoformat()
    })
    item_id = create.json()["id"]
    response = client.get(f"/promo-codes/{item_id}")
    assert response.status_code == 200
    assert response.json()["code"] == "SPRING15"

def test_update_promo_code():
    create = client.post("/promo-codes/", json={
        "code": "NEW10",
        "discount": 10,
        "discount_type": "percent",
        "expiry": (datetime.now() + timedelta(days=7)).isoformat()
    })
    item_id = create.json()["id"]
    response = client.put(f"/promo-codes/{item_id}", json={
        "code": "NEW15",
        "discount": 15,
        "discount_type": "percent",
        "expiry": (datetime.now() + timedelta(days=7)).isoformat()
    })
    assert response.status_code == 200
    assert response.json()["code"] == "NEW15"
    assert response.json()["discount"] == 15

def test_delete_promo_code():
    create = client.post("/promo-codes/", json={
        "code": "DEC10",
        "discount": 10,
        "discount_type": "percent",
        "expiry": (datetime.now() + timedelta(days=7)).isoformat()
    })
    item_id = create.json()["id"]
    response = client.delete(f"/promo-codes/{item_id}")
    assert response.status_code == 204

def test_apply_percent_promo_code():
    create = client.post("/promo-codes/", json={
        "code": "SAVE10",
        "discount": 10,
        "discount_type": "percent",
        "expiry": (datetime.now() + timedelta(days=7)).isoformat()
    })

    response = client.get("/promo-codes/apply/SAVE10", params={"total": 19.48})
    assert response.status_code == 200
    assert response.json()["final_price"] == 17.53

def test_apply_flat_promo_code():
    create = client.post("/promo-codes/", json={
        "code": "SAVE5",
        "discount": 5,
        "discount_type": "flat",
        "expiry": (datetime.now() + timedelta(days=7)).isoformat()
    })
    response = client.get("/promo-codes/apply/SAVE5", params={"total": 29.42})
    assert response.status_code == 200
    assert response.json()["final_price"] == 24.42

def test_apply_expired_promo_code():
    create = client.post("/promo-codes/", json={
        "code": "SAVE10",
        "discount": 10,
        "discount_type": "percent",
        "expiry": (datetime.now() - timedelta(days=7)).isoformat()
    })

    response = client.get("/promo-codes/apply/SAVE10", params={"total": 14.48})
    assert response.status_code == 400

def test_apply_invalid_promo_code():
    response = client.get("/promo-codes/apply/INVALID", params={"total": 14.48})
    assert response.status_code == 404