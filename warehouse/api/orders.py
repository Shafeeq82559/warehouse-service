from fastapi import APIRouter, Depends

from warehouse.api.security import require_api_key
from warehouse.repository import store
from warehouse.schemas import OrderIn
from warehouse.services.order_service import OrderService
from warehouse.services.reports import inventory_valuation

router = APIRouter(tags=["orders"])


def _orders() -> OrderService:
    return OrderService(store)


@router.post("/orders", status_code=201, dependencies=[Depends(require_api_key)])
def place_order(payload: OrderIn):
    return _orders().place_order([(line.sku, line.quantity) for line in payload.lines])


@router.get("/orders/{order_id}")
def get_order(order_id: int):
    return _orders().get(order_id)


@router.post("/orders/{order_id}/cancel", dependencies=[Depends(require_api_key)])
def cancel_order(order_id: int):
    return _orders().cancel_order(order_id)


@router.get("/reports/valuation")
def valuation():
    return inventory_valuation(store)
