from warehouse.models import Order, Product, StockMovement


class InMemoryStore:
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.products: dict[str, Product] = {}
        self.movements: list[StockMovement] = []
        self.orders: dict[int, Order] = {}
        self._next_order_id = 1

    def next_order_id(self) -> int:
        order_id = self._next_order_id
        self._next_order_id += 1
        return order_id


store = InMemoryStore()
