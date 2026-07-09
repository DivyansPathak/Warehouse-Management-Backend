from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.roles import require_roles
from app.modules.sales.schemas import (
    CreateSaleRequest,
)
from app.modules.sales.service import SalesService

router = APIRouter(
    prefix="/sales",
    tags=["Sales"],
)


@router.post("/")
async def create_sale(
    request: CreateSaleRequest,
    current_user: dict = Depends(
        require_roles(
            "admin",
            "manager",
        )
    ),
):
    try:

        sale_id = await SalesService.create_sale(
            request,
            current_user,
        )

        return {
            "message": "Sale created successfully",
            "sale_id": sale_id,
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/")
async def get_all_sales(
    current_user: dict = Depends(
        require_roles(
            "admin",
            "manager",
            "store_keeper",
        )
    ),
):
    return await SalesService.get_all_sales()


@router.get("/{sale_id}")
async def get_sale(
    sale_id: str,
    current_user: dict = Depends(
        require_roles(
            "admin",
            "manager",
            "store_keeper",
        )
    ),
):
    sale = await SalesService.get_sale_by_id(
        sale_id,
    )

    if sale is None:

        raise HTTPException(
            status_code=404,
            detail="Sale not found",
        )

    return sale