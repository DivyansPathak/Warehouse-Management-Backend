from pydantic import BaseModel


class StockInRequest(BaseModel):
    product_id: str
    quantity: int
    remarks: str


class StockOutRequest(BaseModel):
    product_id: str
    quantity: int
    remarks: str


class UpdateReorderLevelRequest(BaseModel):
    reorder_level: int