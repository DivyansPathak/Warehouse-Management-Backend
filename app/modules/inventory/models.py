from datetime import datetime

from pydantic import BaseModel, Field


class Inventory(BaseModel):
    product_id: str

    current_stock: int = 0
    reorder_level: int = 10

    updated_at: datetime = Field(default_factory=datetime.utcnow)


class StockTransaction(BaseModel):
    product_id: str

    transaction_type: str

    quantity: int

    remarks: str

    created_by: str

    created_at: datetime = Field(default_factory=datetime.utcnow)