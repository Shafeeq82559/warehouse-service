from datetime import datetime, timezone

from warehouse.errors import InvalidRequestError, NotFoundError
from warehouse.models import Product, StockMovement
from warehouse.repository import InMemoryStore


class StockService:
    def __init__(self, store: InMemoryStore) -> None:
        self._store = store

    def _product(self, sku: str) -> Product:
        product = self._store.products.get(sku)
        if product is None:
            raise NotFoundError(f"No product with SKU {sku}")
        return product

    def receive(self, sku: str, quantity: int) -> Product:
        if quantity <= 0:
            raise InvalidRequestError("Received quantity must be above zero")
        product = self._product(sku)
        product.quantity_on_hand += quantity
        self._record(sku, "receipt", quantity, None)
        return product

    def adjust(self, sku: str, change: int, reason_code: str) -> Product:
        if not reason_code.strip():
            raise InvalidRequestError("An adjustment needs a reason code")
        product = self._product(sku)
        product.quantity_on_hand += change
        self._record(sku, "adjustment", change, reason_code)
        return product

    def movements_for(self, sku: str) -> list[StockMovement]:
        self._product(sku)
        return [m for m in self._store.movements if m.sku == sku]

    def _record(self, sku: str, kind: str, change: int, reason: str | None) -> None:
        self._store.movements.append(
            StockMovement(sku=sku, kind=kind, change=change, reason=reason, at=datetime.now(timezone.utc))
        )
