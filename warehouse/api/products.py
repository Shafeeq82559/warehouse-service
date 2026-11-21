from fastapi import APIRouter, Depends

from warehouse.api.security import require_api_key
from warehouse.repository import store
from warehouse.schemas import AdjustIn, ProductIn, ReceiveIn
from warehouse.services.product_service import ProductService
from warehouse.services.stock_service import StockService

router = APIRouter(prefix="/products", tags=["products"])


def _products() -> ProductService:
    return ProductService(store)


def _stock() -> StockService:
    return StockService(store)


@router.post("", status_code=201, dependencies=[Depends(require_api_key)])
def add_product(payload: ProductIn):
    return _products().add_product(payload.sku, payload.name, payload.unit_price, payload.min_stock)


@router.get("")
def list_products():
    return _products().list_all()


@router.get("/running-low")
def running_low():
    return _products().running_low()


@router.get("/{sku}")
def get_product(sku: str):
    return _products().get(sku)


@router.delete("/{sku}", status_code=204, dependencies=[Depends(require_api_key)])
def delete_product(sku: str):
    _products().delete_product(sku)


@router.post("/{sku}/receive", dependencies=[Depends(require_api_key)])
def receive_stock(sku: str, payload: ReceiveIn):
    return _stock().receive(sku, payload.quantity)


@router.post("/{sku}/adjust", dependencies=[Depends(require_api_key)])
def adjust_stock(sku: str, payload: AdjustIn):
    return _stock().adjust(sku, payload.change, payload.reason_code)


@router.get("/{sku}/movements")
def stock_movements(sku: str):
    return _stock().movements_for(sku)
