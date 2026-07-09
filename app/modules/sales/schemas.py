from pydantic import BaseModel

from app.modules.sales.models import SaleItem


class CreateSaleRequest(BaseModel):
    customer_name: str

    items: list[SaleItem]

    remarks: str | None = None


class UpdateSaleRequest(BaseModel):
    customer_name: str

    remarks: str | None = None


class SaleResponse(BaseModel):
    id: str

    sale_number: str

    customer_name: str

    items: list[SaleItem]

    total_amount: float

    remarks: str | None

    created_by: str

    created_at: str