def _add(client, headers, sku="A-100", price="4.50", min_stock=5):
    return client.post(
        "/products",
        json={"sku": sku, "name": "Widget", "unit_price": price, "min_stock": min_stock},
        headers=headers,
    )


def test_add_product(client, headers):
    response = _add(client, headers)
    assert response.status_code == 201
    assert response.json()["sku"] == "A-100"


def test_duplicate_sku_is_refused(client, headers):
    _add(client, headers)
    response = _add(client, headers)
    assert response.status_code == 409


def test_write_without_key_is_refused(client):
    response = client.post(
        "/products", json={"sku": "B-1", "name": "Gadget", "unit_price": "1.00", "min_stock": 1}
    )
    assert response.status_code == 401


def test_running_low_lists_products_at_or_under_their_threshold(client, headers):
    _add(client, headers, sku="LOW-1", min_stock=5)
    _add(client, headers, sku="OK-1", min_stock=5)
    client.post("/products/OK-1/receive", json={"quantity": 50}, headers=headers)
    skus = [p["sku"] for p in client.get("/products/running-low").json()]
    assert skus == ["LOW-1"]
