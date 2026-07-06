from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.roles import require_roles
from app.modules.inventory.schemas import (
    StockInRequest,
    StockOutRequest,
)
from app.modules.inventory.service import InventoryService

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
)


@router.post("/stock-in")
async def stock_in(
    request: StockInRequest,
    current_user: dict = Depends(
        require_roles("admin", "manager"),
    ),
):
    await InventoryService.stock_in(
        request,
        current_user,
    )

    return {
        "message": "Stock added successfully",
    }


@router.post("/stock-out")
async def stock_out(
    request: StockOutRequest,
    current_user: dict = Depends(
        require_roles("admin", "manager"),
    ),
):
    try:
        await InventoryService.stock_out(
            request,
            current_user,
        )

        return {
            "message": "Stock issued successfully",
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/")
async def get_all_inventory(
    current_user: dict = Depends(
        require_roles(
            "admin",
            "manager",
            "store_keeper",
        ),
    ),
):
    return await InventoryService.get_all_inventory()


@router.get("/low-stock")
async def get_low_stock(
    current_user: dict = Depends(
        require_roles(
            "admin",
            "manager",
        ),
    ),
):
    return await InventoryService.get_low_stock()


@router.get("/{product_id}")
async def get_inventory(
    product_id: str,
    current_user: dict = Depends(
        require_roles(
            "admin",
            "manager",
            "store_keeper",
        ),
    ),
):
    return await InventoryService.get_inventory(
        product_id,
    )


@router.get("/{product_id}/history")
async def get_stock_history(
    product_id: str,
    current_user: dict = Depends(
        require_roles(
            "admin",
            "manager",
            "store_keeper",
        ),
    ),
):
    return await InventoryService.get_stock_history(
        product_id,
    )