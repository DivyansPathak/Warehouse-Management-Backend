from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.roles import require_roles
from app.modules.suppliers.schemas import (
    CreateSupplierRequest,
    UpdateSupplierRequest,
)
from app.modules.suppliers.service import SupplierService

router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"],
)


@router.post("/")
async def create_supplier(
    request: CreateSupplierRequest,
    current_user: dict = Depends(
        require_roles(
            "admin",
            "manager",
        ),
    ),
):
    try:
        supplier_id = await SupplierService.create_supplier(
            request,
        )

        return {
            "message": "Supplier created successfully",
            "supplier_id": supplier_id,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/")
async def get_all_suppliers(
    current_user: dict = Depends(
        require_roles(
            "admin",
            "manager",
            "store_keeper",
        ),
    ),
):
    return await SupplierService.get_all_suppliers()


@router.get("/{supplier_id}")
async def get_supplier(
    supplier_id: str,
    current_user: dict = Depends(
        require_roles(
            "admin",
            "manager",
            "store_keeper",
        ),
    ),
):
    supplier = await SupplierService.get_supplier_by_id(
        supplier_id,
    )

    if not supplier:
        raise HTTPException(
            status_code=404,
            detail="Supplier not found",
        )

    return supplier


@router.put("/{supplier_id}")
async def update_supplier(
    supplier_id: str,
    request: UpdateSupplierRequest,
    current_user: dict = Depends(
        require_roles(
            "admin",
            "manager",
        ),
    ),
):
    await SupplierService.update_supplier(
        supplier_id,
        request,
    )

    return {
        "message": "Supplier updated successfully",
    }


@router.delete("/{supplier_id}")
async def delete_supplier(
    supplier_id: str,
    current_user: dict = Depends(
        require_roles(
            "admin",
        ),
    ),
):
    await SupplierService.delete_supplier(
        supplier_id,
    )

    return {
        "message": "Supplier deleted successfully",
    }