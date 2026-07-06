from datetime import datetime

from app.modules.inventory.models import Inventory, StockTransaction
from app.modules.inventory.repository import InventoryRepository
from app.modules.purchase_orders.models import PurchaseOrder
from app.modules.purchase_orders.repository import PurchaseOrderRepository
from app.utils.mongo import serialize_document, serialize_documents


class PurchaseOrderService:

    @staticmethod
    async def create_purchase_order(
        request,
        current_user,
    ):

        po_count = await PurchaseOrderRepository.count()

        po_number = f"PO-{po_count + 1:04d}"

        purchase_order = PurchaseOrder(
            po_number=po_number,
            supplier_id=request.supplier_id,
            items=request.items,
            remarks=request.remarks,
            created_by=current_user["email"],
        )

        result = await PurchaseOrderRepository.create(
            purchase_order.model_dump(),
        )

        return str(result.inserted_id)

    @staticmethod
    async def get_all_purchase_orders():

        purchase_orders = await PurchaseOrderRepository.get_all()

        return serialize_documents(
            purchase_orders,
        )

    @staticmethod
    async def get_purchase_order_by_id(
        purchase_order_id: str,
    ):

        purchase_order = await PurchaseOrderRepository.get_by_id(
            purchase_order_id,
        )

        return serialize_document(
            purchase_order,
        )

    @staticmethod
    async def update_status(
        purchase_order_id: str,
        request,
    ):

        await PurchaseOrderRepository.update(
            purchase_order_id,
            {
                "status": request.status,
                "updated_at": datetime.utcnow(),
            },
        )

    @staticmethod
    async def receive_purchase_order(
        purchase_order_id: str,
        request,
        current_user,
    ):

        purchase_order = await PurchaseOrderRepository.get_by_id(
            purchase_order_id,
        )

        if purchase_order is None:
            raise ValueError(
                "Purchase Order not found",
            )

        if purchase_order["status"] == "RECEIVED":
            raise ValueError(
                "Purchase Order already received",
            )

        for item in purchase_order["items"]:

            inventory = await InventoryRepository.get_inventory_by_product_id(
                item["product_id"],
            )

            if inventory is None:

                inventory = Inventory(
                    product_id=item["product_id"],
                    current_stock=item["quantity"],
                )

                await InventoryRepository.create_inventory(
                    inventory.model_dump(),
                )

            else:

                await InventoryRepository.update_inventory(
                    item["product_id"],
                    {
                        "current_stock": inventory["current_stock"] + item["quantity"],
                    },
                )

            transaction = StockTransaction(
                product_id=item["product_id"],
                transaction_type="IN",
                quantity=item["quantity"],
                remarks=request.remarks,
                created_by=current_user["email"],
            )

            await InventoryRepository.create_transaction(
                transaction.model_dump(),
            )

        await PurchaseOrderRepository.update(
            purchase_order_id,
            {
                "status": "RECEIVED",
                "updated_at": datetime.utcnow(),
            },
        )