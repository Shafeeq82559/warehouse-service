def _stocked(client, headers, quantity=20):
    client.post(
        "/products",
        json={"sku": "O-1", "name": "Panel", "unit_price": "12.00", "min_stock": 2},
        headers=headers,
    )
    client.post("/products/O-1/receive", json={"quantity": quantity}, headers=headers)


def test_order_reduces_stock(client, headers):
    _stocked(client, headers)
    response = client.post("/orders", json={"lines": [{"sku": "O-1", "quantity": 5}]}, headers=headers)
    assert response.status_code == 201
    assert float(response.json()["total"]) == 60.0
    assert client.get("/products/O-1").json()["quantity_on_hand"] == 15


def test_order_is_refused_when_stock_is_short(client, headers):
    _stocked(client, headers, quantity=3)
    response = client.post("/orders", json={"lines": [{"sku": "O-1", "quantity": 4}]}, headers=headers)
    assert response.status_code == 409
    assert client.get("/products/O-1").json()["quantity_on_hand"] == 3


def test_cancel_returns_stock(client, headers):
    _stocked(client, headers)
    order = client.post("/orders", json={"lines": [{"sku": "O-1", "quantity": 5}]}, headers=headers).json()
    client.post(f"/orders/{order['id']}/cancel", headers=headers)
    assert client.get("/products/O-1").json()["quantity_on_hand"] == 20
