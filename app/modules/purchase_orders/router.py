from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.roles import require_roles
from app.modules.purchase_orders.schemas import (
    CreatePurchaseOrderRequest,
    ReceivePurchaseOrderRequest,
    UpdatePurchaseOrderStatusRequest,
)
from app.modules.purchase_orders.service import PurchaseOrderService

router = APIRouter(
    prefix="/purchase-orders",
    tags=["Purchase Orders"],
)


@router.post("/")
async def create_purchase_order(
    request: CreatePurchaseOrderRequest,
    current_user: dict = Depends(
        require_roles(
            "admin",
            "manager",
        )
    ),
):
    purchase_order_id = await PurchaseOrderService.create_purchase_order(
        request,
        current_user,
    )

    return {
        "message": "Purchase Order created successfully",
        "purchase_order_id": purchase_order_id,
    }


@router.get("/")
async def get_all_purchase_orders(
    current_user: dict = Depends(
        require_roles(
            "admin",
            "manager",
            "store_keeper",
        )
    ),
):
    return await PurchaseOrderService.get_all_purchase_orders()


@router.get("/{purchase_order_id}")
async def get_purchase_order(
    purchase_order_id: str,
    current_user: dict = Depends(
        require_roles(
            "admin",
            "manager",
            "store_keeper",
        )
    ),
):
    return await PurchaseOrderService.get_purchase_order_by_id(
        purchase_order_id
    )


@router.put("/{purchase_order_id}/status")
async def update_status(
    purchase_order_id: str,
    request: UpdatePurchaseOrderStatusRequest,
    current_user: dict = Depends(
        require_roles(
            "admin",
            "manager",
        )
    ),
):
    await PurchaseOrderService.update_status(
        purchase_order_id,
        request,
    )

    return {
        "message": "Purchase Order updated successfully",
    }


@router.post("/{purchase_order_id}/receive")
async def receive_purchase_order(
    purchase_order_id: str,
    request: ReceivePurchaseOrderRequest,
    current_user: dict = Depends(
        require_roles(
            "admin",
            "manager",
        )
    ),
):
    try:

        await PurchaseOrderService.receive_purchase_order(
            purchase_order_id,
            request,
            current_user,
        )

        return {
            "message": "Purchase Order received successfully",
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )