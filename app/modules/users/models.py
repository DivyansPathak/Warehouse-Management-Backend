from datetime import datetime

from pydantic import BaseModel, EmailStr, Field
from typing import Literal


class AppUser(BaseModel):
    name: str
    email: EmailStr
    password: str

    role: Literal[
        "admin",
        "manager",
        "store_keeper",
    ]

    is_active: bool = True

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)