from datetime import datetime

from pydantic import BaseModel, Field


class PurchaseOrderItem(BaseModel):
    product_id: str
    quantity: int
    purchase_price: float


class PurchaseOrder(BaseModel):
    po_number: str

    supplier_id: str

    items: list[PurchaseOrderItem]

    status: str = "PENDING"

    remarks: str | None = None

    created_by: str

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)