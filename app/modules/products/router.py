from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.roles import require_roles
from app.modules.products.schemas import (
    CreateProductRequest,
    UpdateProductRequest,
)
from app.modules.products.service import ProductService

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post("/")
async def create_product(
    request: CreateProductRequest,
    current_user: dict = Depends(require_roles("admin", "manager")),
):
    product_id = await ProductService.create_product(request)

    return {
        "message": "Product created successfully",
        "product_id": product_id,
    }


@router.get("/")
async def get_all_products(
    current_user: dict = Depends(
        require_roles(
            "admin",
            "manager",
            "store_keeper",
        )
    ),
):
    return await ProductService.get_all_products()


@router.get("/{product_id}")
async def get_product(
    product_id: str,
    current_user: dict = Depends(
        require_roles(
            "admin",
            "manager",
            "store_keeper",
        )
    ),
):
    product = await ProductService.get_product_by_id(product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return product


@router.put("/{product_id}")
async def update_product(
    product_id: str,
    request: UpdateProductRequest,
    current_user: dict = Depends(
        require_roles("admin", "manager")
    ),
):
    await ProductService.update_product(
        product_id,
        request,
    )

    return {
        "message": "Product updated successfully",
    }


@router.delete("/{product_id}")
async def delete_product(
    product_id: str,
    current_user: dict = Depends(
        require_roles("admin")
    ),
):
    await ProductService.delete_product(product_id)

    return {
        "message": "Product deleted successfully",
    }