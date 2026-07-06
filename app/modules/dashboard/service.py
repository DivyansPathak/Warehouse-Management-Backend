from app.modules.inventory.repository import InventoryRepository
from app.modules.products.repository import ProductRepository
from app.modules.purchase_orders.repository import PurchaseOrderRepository
from app.modules.suppliers.repository import SupplierRepository
from app.utils.mongo import (
    serialize_dashboard_documents,
    serialize_documents,
)


class DashboardService:

    @staticmethod
    async def get_dashboard():

        total_products = await ProductRepository.count()

        total_suppliers = await SupplierRepository.count()

        total_purchase_orders = await PurchaseOrderRepository.count()

        pending_purchase_orders = (
            await PurchaseOrderRepository.get_pending_count()
        )

        low_stock_items = (
            await InventoryRepository.get_low_stock_count()
        )

        inventory_value = (
            await InventoryRepository.get_inventory_value()
        )

        return {
            "total_products": total_products,
            "total_suppliers": total_suppliers,
            "total_purchase_orders": total_purchase_orders,
            "pending_purchase_orders": pending_purchase_orders,
            "low_stock_items": low_stock_items,
            "inventory_value": round(
                inventory_value,
                2,
            ),
        }

    @staticmethod
    async def get_charts():

        category_distribution = (
            await InventoryRepository.get_category_distribution()
        )

        inventory_by_category = [
            {
                "category": item["_id"],
                "units": item["units"],
            }
            for item in category_distribution
        ]

        revenue = (
            await InventoryRepository.get_inventory_value_last_10_days()
        )

        orders = (
            await PurchaseOrderRepository.get_orders_last_10_days()
        )

        order_map = {
            item["date"]: item["orders"]
            for item in orders
        }

        revenue_vs_orders = [
            {
                "date": item["date"],
                "revenue": round(
                    item["revenue"],
                    2,
                ),
                "orders": order_map.get(
                    item["date"],
                    0,
                ),
            }
            for item in revenue
        ]

        return {
            "inventory_by_category": inventory_by_category,
            "revenue_vs_orders": revenue_vs_orders,
        }

    @staticmethod
    async def get_recent():

        transactions = (
            await InventoryRepository.get_recent_transactions()
        )

        purchase_orders = (
            await PurchaseOrderRepository.get_recent()
        )

        return {
            "transactions": serialize_dashboard_documents(
                transactions,
            ),
            "purchase_orders": serialize_dashboard_documents(
                purchase_orders,
            ),
        }

    @staticmethod
    async def get_alerts():

        low_stock = (
            await InventoryRepository.get_low_stock_items()
        )

        pending_purchase_orders = (
            await PurchaseOrderRepository.get_pending()
        )

        return {
            "low_stock": serialize_documents(
                low_stock,
            ),
            "pending_purchase_orders": serialize_dashboard_documents(
                pending_purchase_orders,
            ),
        }