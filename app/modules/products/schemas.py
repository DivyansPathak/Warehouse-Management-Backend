from pydantic import BaseModel


class CreateProductRequest(BaseModel):
    name: str
    sku: str
    description: str

    category: str
    unit: str

    purchase_price: float
    selling_price: float

    supplier_id: str | None = None


class UpdateProductRequest(BaseModel):
    name: str
    sku: str
    description: str

    category: str
    unit: str

    purchase_price: float
    selling_price: float

    supplier_id: str | None = None

    is_active: bool


class ProductResponse(BaseModel):
    id: str

    name: str
    sku: str
    description: str

    category: str
    unit: str

    purchase_price: float
    selling_price: float

    supplier_id: str | None

    is_active: bool