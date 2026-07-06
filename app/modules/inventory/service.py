from app.modules.inventory.models import Inventory, StockTransaction
from app.modules.inventory.repository import InventoryRepository
from app.utils.mongo import serialize_document, serialize_documents


class InventoryService:

    @staticmethod
    async def stock_in(
        request,
        current_user,
    ):

        inventory = await InventoryRepository.get_inventory_by_product_id(
            request.product_id,
        )

        if inventory is None:

            inventory = Inventory(
                product_id=request.product_id,
                current_stock=request.quantity,
            )

            await InventoryRepository.create_inventory(
                inventory.model_dump(),
            )

        else:

            await InventoryRepository.update_inventory(
                request.product_id,
                {
                    "current_stock": inventory["current_stock"] + request.quantity,
                },
            )

        transaction = StockTransaction(
            product_id=request.product_id,
            transaction_type="IN",
            quantity=request.quantity,
            remarks=request.remarks,
            created_by=current_user["email"],
        )

        await InventoryRepository.create_transaction(
            transaction.model_dump(),
        )

    @staticmethod
    async def stock_out(
        request,
        current_user,
    ):

        inventory = await InventoryRepository.get_inventory_by_product_id(
            request.product_id,
        )

        if inventory is None:
            raise ValueError("Inventory not found")

        if inventory["current_stock"] < request.quantity:
            raise ValueError("Insufficient stock")

        await InventoryRepository.update_inventory(
            request.product_id,
            {
                "current_stock": inventory["current_stock"] - request.quantity,
            },
        )

        transaction = StockTransaction(
            product_id=request.product_id,
            transaction_type="OUT",
            quantity=request.quantity,
            remarks=request.remarks,
            created_by=current_user["email"],
        )

        await InventoryRepository.create_transaction(
            transaction.model_dump(),
        )

    @staticmethod
    async def get_inventory(product_id: str):

        inventory = await InventoryRepository.get_inventory_by_product_id(
            product_id,
        )

        return serialize_document(inventory)

    @staticmethod
    async def get_all_inventory():

        inventory = await InventoryRepository.get_all_inventory()

        return serialize_documents(inventory)

    @staticmethod
    async def get_stock_history(product_id: str):

        transactions = await InventoryRepository.get_transactions(
            product_id,
        )

        return serialize_documents(transactions)

    @staticmethod
    async def get_low_stock():

        inventory = await InventoryRepository.get_low_stock_items()

        low_stock = []

        for item in inventory:
            if item["current_stock"] <= item["reorder_level"]:
                low_stock.append(item)

        return serialize_documents(low_stock)