from typing import Literal

from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

    role: Literal[
        "manager",
        "store_keeper",
    ]


class UpdateUserRequest(BaseModel):
    name: str
    email: EmailStr

    role: Literal[
        "manager",
        "store_keeper",
    ]

    is_active: bool


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str
    is_active: bool