from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.roles import require_roles
from app.modules.users.schemas import (
    CreateUserRequest,
    UpdateUserRequest,
)
from app.modules.users.service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/")
async def create_user(
    request: CreateUserRequest,
    current_user: dict = Depends(
        require_roles("admin"),
    ),
):
    try:
        user_id = await UserService.create_user(
            request,
        )

        return {
            "message": "User created successfully",
            "user_id": user_id,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/")
async def get_all_users(
    current_user: dict = Depends(
        require_roles("admin"),
    ),
):
    return await UserService.get_all_users()


@router.get("/{user_id}")
async def get_user(
    user_id: str,
    current_user: dict = Depends(
        require_roles("admin"),
    ),
):
    user = await UserService.get_user_by_id(
        user_id,
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


@router.put("/{user_id}")
async def update_user(
    user_id: str,
    request: UpdateUserRequest,
    current_user: dict = Depends(
        require_roles("admin"),
    ),
):
    await UserService.update_user(
        user_id,
        request,
    )

    return {
        "message": "User updated successfully",
    }


@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    current_user: dict = Depends(
        require_roles("admin"),
    ),
):
    await UserService.delete_user(
        user_id,
    )

    return {
        "message": "User deleted successfully",
    }