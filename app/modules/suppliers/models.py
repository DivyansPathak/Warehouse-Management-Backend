from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class Supplier(BaseModel):
    name: str
    contact_person: str

    email: EmailStr
    phone: str

    address: str

    is_active: bool = True

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)