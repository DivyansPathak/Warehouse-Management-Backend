from pydantic import BaseModel, EmailStr


class CreateSupplierRequest(BaseModel):
    name: str
    contact_person: str

    email: EmailStr
    phone: str

    address: str


class UpdateSupplierRequest(BaseModel):
    name: str
    contact_person: str

    email: EmailStr
    phone: str

    address: str

    is_active: bool


class SupplierResponse(BaseModel):
    id: str

    name: str
    contact_person: str

    email: EmailStr
    phone: str

    address: str

    is_active: bool