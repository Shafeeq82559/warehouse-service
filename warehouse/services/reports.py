from decimal import Decimal

from warehouse.repository import InMemoryStore


def inventory_valuation(store: InMemoryStore) -> dict:
    rows = []
    total_value = Decimal("0")
    for product in sorted(store.products.values(), key=lambda p: p.sku):
        value = product.unit_price * product.quantity_on_hand
        total_value += value
        rows.append({"sku": product.sku, "quantity": product.quantity_on_hand, "value": value})
    return {"total_value": total_value, "products": rows}
