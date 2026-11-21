from decimal import Decimal

from pydantic import BaseModel, Field


class ProductIn(BaseModel):
    sku: str = Field(min_length=1, max_length=40)
    name: str = Field(min_length=1, max_length=120)
    unit_price: Decimal = Field(gt=0)
    min_stock: int = Field(ge=0)


class ReceiveIn(BaseModel):
    quantity: int = Field(gt=0)


class AdjustIn(BaseModel):
    change: int
    reason_code: str = Field(min_length=1, max_length=40)


class LineIn(BaseModel):
    sku: str = Field(min_length=1)
    quantity: int = Field(gt=0)


class OrderIn(BaseModel):
    lines: list[LineIn] = Field(min_length=1)
