from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    name: str
    email: EmailStr
    password: str

    role: Literal["admin", "manager", "store_keeper"] = "store_keeper"

    is_active: bool = True

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)