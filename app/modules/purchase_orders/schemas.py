from pydantic import BaseModel

from app.modules.purchase_orders.models import PurchaseOrderItem


class CreatePurchaseOrderRequest(BaseModel):
    supplier_id: str
    items: list[PurchaseOrderItem]
    remarks: str | None = None


class UpdatePurchaseOrderStatusRequest(BaseModel):
    status: str


class ReceivePurchaseOrderRequest(BaseModel):
    remarks: str