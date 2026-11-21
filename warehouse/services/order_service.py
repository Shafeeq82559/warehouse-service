from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal

from warehouse.errors import ConflictError, InvalidRequestError, NotFoundError
from warehouse.models import Order, OrderLine
from warehouse.repository import InMemoryStore


class OrderService:
    def __init__(self, store: InMemoryStore) -> None:
        self._store = store

    def place_order(self, lines: list[tuple[str, int]]) -> Order:
        if not lines:
            raise InvalidRequestError("An order needs at least one line")

        wanted: dict[str, int] = defaultdict(int)
        for sku, quantity in lines:
            if quantity <= 0:
                raise InvalidRequestError("Line quantities must be above zero")
            wanted[sku] += quantity

        for sku, quantity in wanted.items():
            product = self._store.products.get(sku)
            if product is None:
                raise NotFoundError(f"No product with SKU {sku}")
            if product.quantity_on_hand < quantity:
                raise ConflictError(f"Not enough stock for {sku}")

        order_lines = []
        total = Decimal("0")
        for sku, quantity in wanted.items():
            product = self._store.products[sku]
            product.quantity_on_hand -= quantity
            order_lines.append(OrderLine(sku=sku, quantity=quantity, unit_price=product.unit_price))
            total += product.unit_price * quantity

        order = Order(
            id=self._store.next_order_id(),
            lines=order_lines,
            status="placed",
            total=total,
            placed_at=datetime.now(timezone.utc),
        )
        self._store.orders[order.id] = order
        return order

    def get(self, order_id: int) -> Order:
        order = self._store.orders.get(order_id)
        if order is None:
            raise NotFoundError(f"No order with id {order_id}")
        return order

    def cancel_order(self, order_id: int) -> Order:
        order = self.get(order_id)
        if order.status == "cancelled":
            raise ConflictError(f"Order {order_id} is already cancelled")
        for line in order.lines:
            product = self._store.products.get(line.sku)
            if product is not None:
                product.quantity_on_hand += line.quantity
        order.status = "cancelled"
        return order
