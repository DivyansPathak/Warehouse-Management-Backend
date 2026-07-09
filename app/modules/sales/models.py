from datetime import datetime

from pydantic import BaseModel, Field


class SaleItem(BaseModel):
    product_id: str
    quantity: int
    selling_price: float


class Sale(BaseModel):
    sale_number: str

    customer_name: str

    items: list[SaleItem]

    total_amount: float

    remarks: str | None = None

    created_by: str

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
    )