def _product(client, headers):
    client.post(
        "/products",
        json={"sku": "S-1", "name": "Bolt", "unit_price": "0.20", "min_stock": 10},
        headers=headers,
    )


def test_receive_adds_to_stock(client, headers):
    _product(client, headers)
    response = client.post("/products/S-1/receive", json={"quantity": 40}, headers=headers)
    assert response.json()["quantity_on_hand"] == 40


def test_receive_needs_positive_quantity(client, headers):
    _product(client, headers)
    response = client.post("/products/S-1/receive", json={"quantity": 0}, headers=headers)
    assert response.status_code == 422


def test_adjustment_needs_a_reason(client, headers):
    _product(client, headers)
    response = client.post("/products/S-1/adjust", json={"change": -1, "reason_code": ""}, headers=headers)
    assert response.status_code == 422


def test_movements_are_listed(client, headers):
    _product(client, headers)
    client.post("/products/S-1/receive", json={"quantity": 10}, headers=headers)
    client.post("/products/S-1/adjust", json={"change": -2, "reason_code": "DAMAGE"}, headers=headers)
    movements = client.get("/products/S-1/movements").json()
    assert [m["kind"] for m in movements] == ["receipt", "adjustment"]
