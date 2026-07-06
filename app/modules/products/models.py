from datetime import datetime

from pydantic import BaseModel, Field


class Product(BaseModel):
    name: str
    sku: str
    description: str

    category: str
    unit: str

    purchase_price: float
    selling_price: float

    supplier_id: str | None = None

    is_active: bool = True

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)