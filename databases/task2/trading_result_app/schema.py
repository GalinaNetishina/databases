import datetime

from pydantic import BaseModel, Field


class TradingDay(BaseModel):
    date: datetime.date


class ItemDTO(TradingDay, BaseModel):
    exchange_product_id: str
    exchange_product_name: str
    delivery_basis_name: str
    volume: int = Field(gt=0)
    total: int = Field(gt=0)
    count: int = Field(gt=0)


class ItemFull(ItemDTO):
    oil_id: str
    delivery_basis_id: str
    delivery_type_id: str
    created_on: datetime.datetime
    updated_on: datetime.datetime
