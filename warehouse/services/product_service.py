from decimal import Decimal

from warehouse.errors import ConflictError, NotFoundError
from warehouse.models import Product
from warehouse.repository import InMemoryStore


class ProductService:
    def __init__(self, store: InMemoryStore) -> None:
        self._store = store

    def add_product(self, sku: str, name: str, unit_price: Decimal, min_stock: int) -> Product:
        if sku in self._store.products:
            raise ConflictError(f"A product with SKU {sku} already exists")
        product = Product(sku=sku, name=name, unit_price=unit_price, min_stock=min_stock)
        self._store.products[sku] = product
        return product

    def get(self, sku: str) -> Product:
        product = self._store.products.get(sku)
        if product is None:
            raise NotFoundError(f"No product with SKU {sku}")
        return product

    def list_all(self) -> list[Product]:
        return sorted(self._store.products.values(), key=lambda p: p.sku)

    def delete_product(self, sku: str) -> None:
        self.get(sku)
        del self._store.products[sku]

    def running_low(self) -> list[Product]:
        return [p for p in self.list_all() if p.quantity_on_hand <= p.min_stock]
