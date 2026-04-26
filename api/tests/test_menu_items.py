from fastapi.testclient import TestClient
from ..controllers import orders as controller
from ..main import app
import pytest
from ..models import orders as model


def test_create_menu_item(client):
   response = client.post("/menu_items/", json={
       "name": "Cheese Burger",
       "price": 7.99,
       "category": "Entrees",
       "calories": 500
   })
   assert response.status_code == 200
   assert response.json()["name"] == "Cheese Burger"


def test_read_all_menu_items(client):
   response = client.get("/menu_items/")
   assert response.status_code == 200
   assert isinstance(response.json(), list)


def test_read_one_menu_item(client):
   create = client.post("/menu_items/", json={
       "name": "Fries",
       "price": 3.99,
       "category": "Sides",
       "calories": 300
   })
   item_id = create.json()["id"]
   response = client.get(f"/menu_items/{item_id}")
   assert response.status_code == 200
   assert response.json()["name"] == "Fries"


def test_search_menu_item(client):
   create = client.post("/menu_items/", json={
       "name": "Soda",
       "price": 1.99,
       "category": "Drinks",
       "calories": 100
   })
   response = client.get("/menu_items/search?/category=Drinks")
   assert response.status_code == 200


def test_update_menu_item(client):
   create = client.post("/menu_items/", json={
       "name": "Chicken Sandwich",
       "price": 5.99,
       "category": "Entrees",
       "calories": 400
   })
   item_id = create.json()["id"]
   response = client.put(f"/menu_items/{item_id}", json={
       "price": 6.99
   })
   assert response.status_code == 200
   assert response.json()["price"] == 6.99


def test_delete_menu_item(client):
   create = client.post("/menu_items/", json={
       "name": "Potato Chips",
       "price": 1.99,
       "category": "Sides",
       "calories": 100
   })
   item_id = create.json()["id"]
   response = client.delete(f"/menu_items/{item_id}")
   assert response.status_code == 204
