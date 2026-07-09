from app.modules.inventory.models import StockTransaction
from app.modules.inventory.repository import InventoryRepository
from app.modules.sales.models import Sale
from app.modules.sales.repository import SalesRepository
from app.modules.sales.schemas import CreateSaleRequest
from app.utils.mongo import (
    serialize_document,
    serialize_documents,
)


class SalesService:

    @staticmethod
    async def create_sale(
        request: CreateSaleRequest,
        current_user: dict,
    ):

        sale_count = await SalesRepository.count()

        sale_number = f"SALE-{sale_count + 1:04d}"

        total_amount = 0.0

        for item in request.items:

            inventory = (
                await InventoryRepository.get_inventory_by_product_id(
                    item.product_id,
                )
            )

            if inventory is None:
                raise ValueError(
                    f"Inventory not found for Product {item.product_id}",
                )

            if inventory["current_stock"] < item.quantity:
                raise ValueError(
                    f"Insufficient stock for Product {item.product_id}",
                )

            total_amount += (
                item.quantity
                * item.selling_price
            )

        sale = Sale(
            sale_number=sale_number,
            customer_name=request.customer_name,
            items=request.items,
            total_amount=total_amount,
            remarks=request.remarks,
            created_by=current_user["email"],
        )

        result = await SalesRepository.create(
            sale.model_dump(),
        )

        for item in request.items:

            inventory = (
                await InventoryRepository.get_inventory_by_product_id(
                    item.product_id,
                )
            )

            await InventoryRepository.update_inventory(
                item.product_id,
                {
                    "current_stock":
                        inventory["current_stock"]
                        - item.quantity,
                },
            )

            transaction = StockTransaction(
                product_id=item.product_id,
                transaction_type="OUT",
                quantity=item.quantity,
                remarks=f"Sale {sale_number}",
                created_by=current_user["email"],
            )

            await InventoryRepository.create_transaction(
                transaction.model_dump(),
            )

        return str(result.inserted_id)

    @staticmethod
    async def get_all_sales():

        sales = await SalesRepository.get_all()

        return serialize_documents(
            sales,
        )

    @staticmethod
    async def get_sale_by_id(
        sale_id: str,
    ):

        sale = await SalesRepository.get_by_id(
            sale_id,
        )

        return serialize_document(
            sale,
        )

    @staticmethod
    async def update_sale(
        sale_id: str,
        request,
    ):

        await SalesRepository.update(
            sale_id,
            request.model_dump(),
        )

    @staticmethod
    async def delete_sale(
        sale_id: str,
    ):

        await SalesRepository.delete(
            sale_id,
        )