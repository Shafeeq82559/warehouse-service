from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class Product:
    sku: str
    name: str
    unit_price: Decimal
    min_stock: int
    quantity_on_hand: int = 0


@dataclass
class StockMovement:
    sku: str
    kind: str
    change: int
    reason: str | None
    at: datetime


@dataclass
class OrderLine:
    sku: str
    quantity: int
    unit_price: Decimal


@dataclass
class Order:
    id: int
    lines: list[OrderLine]
    status: str
    total: Decimal
    placed_at: datetime
