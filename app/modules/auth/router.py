from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.auth import get_current_user
from app.dependencies.roles import require_roles
from app.modules.auth.schemas import LoginRequest, RegisterRequest
from app.modules.auth.service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register")
async def register(request: RegisterRequest):
    try:
        user_id = await AuthService.register(
            request.name,
            request.email,
            request.password,
        )

        return {
            "message": "User registered successfully",
            "user_id": user_id,
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(request: LoginRequest):
    try:
        return await AuthService.login(
            request.email,
            request.password,
        )

    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/me")
async def get_me(
    current_user: dict = Depends(get_current_user),
):
    return current_user


@router.get("/admin")
async def admin_route(
    current_user: dict = Depends(require_roles("admin")),
):
    return {
        "message": "Welcome Admin",
        "user": current_user,
    }


@router.get("/manager")
async def manager_route(
    current_user: dict = Depends(require_roles("admin", "manager")),
):
    return {
        "message": "Welcome Manager",
        "user": current_user,
    }


@router.get("/store")
async def store_keeper_route(
    current_user: dict = Depends(
        require_roles(
            "admin",
            "manager",
            "store_keeper",
        )
    ),
):
    return {
        "message": "Welcome Store Keeper",
        "user": current_user,
    }