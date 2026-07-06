from app.db.database import database


class InventoryRepository:

    inventory_collection = database["inventory"]
    transaction_collection = database["stock_transactions"]
    product_collection = database["products"]

    @classmethod
    async def create_inventory(cls, inventory: dict):
        return await cls.inventory_collection.insert_one(
            inventory,
        )

    @classmethod
    async def get_inventory_by_product_id(cls, product_id: str):
        return await cls.inventory_collection.find_one(
            {
                "product_id": product_id,
            }
        )

    @classmethod
    async def update_inventory(
        cls,
        product_id: str,
        data: dict,
    ):
        return await cls.inventory_collection.update_one(
            {
                "product_id": product_id,
            },
            {
                "$set": data,
            },
        )

    @classmethod
    async def create_transaction(cls, transaction: dict):
        return await cls.transaction_collection.insert_one(
            transaction,
        )

    @classmethod
    async def get_transactions(cls, product_id: str):
        return await cls.transaction_collection.find(
            {
                "product_id": product_id,
            }
        ).to_list(None)

    @classmethod
    async def get_all_inventory(cls):
        return await cls.inventory_collection.find().to_list(
            None,
        )

    @classmethod
    async def get_low_stock_items(cls):
        return await cls.inventory_collection.find().to_list(
            None,
        )

    @classmethod
    async def get_low_stock_count(cls):

        inventory = await cls.get_all_inventory()

        count = 0

        for item in inventory:
            if item["current_stock"] <= item["reorder_level"]:
                count += 1

        return count

    @classmethod
    async def get_inventory_value(cls):

        pipeline = [
            {
                "$lookup": {
                    "from": "products",
                    "localField": "product_id",
                    "foreignField": "_id",
                    "as": "product",
                },
            },
        ]

        return await cls.inventory_collection.aggregate(
            pipeline,
        ).to_list(None)

    @classmethod
    async def get_category_distribution(cls):

        pipeline = [
            {
                "$lookup": {
                    "from": "products",
                    "localField": "product_id",
                    "foreignField": "_id",
                    "as": "product",
                },
            },
        ]

        return await cls.inventory_collection.aggregate(
            pipeline,
        ).to_list(None)

    @classmethod
    async def get_stock_movement(cls):

        pipeline = [
            {
                "$group": {
                    "_id": {
                        "date": {
                            "$dateToString": {
                                "format": "%Y-%m-%d",
                                "date": "$created_at",
                            },
                        },
                        "type": "$transaction_type",
                    },
                    "quantity": {
                        "$sum": "$quantity",
                    },
                },
            },
            {
                "$sort": {
                    "_id.date": 1,
                },
            },
        ]

        return await cls.transaction_collection.aggregate(
            pipeline,
        ).to_list(None)