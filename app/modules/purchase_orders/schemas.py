from pydantic import BaseModel


class PurchaseOrderItemRequest(BaseModel):
    product_id: str
    quantity: int
    purchase_price: float


class CreatePurchaseOrderRequest(BaseModel):
    supplier_id: str

    items: list[PurchaseOrderItemRequest]

    remarks: str | None = None


class UpdatePurchaseOrderStatusRequest(BaseModel):
    status: str


class ReceivePurchaseOrderRequest(BaseModel):
    remarks: str