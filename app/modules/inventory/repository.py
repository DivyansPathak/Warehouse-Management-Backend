from datetime import datetime, timedelta

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
    async def get_recent_transactions(
        cls,
        limit: int = 10,
    ):
        return await cls.transaction_collection.find().sort(
            "created_at",
            -1,
        ).limit(limit).to_list(limit)

    @classmethod
    async def get_all_inventory(cls):
        return await cls.inventory_collection.find().to_list(
            None,
        )

    @classmethod
    async def get_low_stock_items(cls):
        return await cls.inventory_collection.find(
            {
                "$expr": {
                    "$lte": [
                        "$current_stock",
                        "$reorder_level",
                    ]
                }
            }
        ).to_list(None)

    @classmethod
    async def get_low_stock_count(cls):
        return await cls.inventory_collection.count_documents(
            {
                "$expr": {
                    "$lte": [
                        "$current_stock",
                        "$reorder_level",
                    ]
                }
            }
        )

    @classmethod
    async def get_inventory_value(cls):

        pipeline = [
    {
        "$addFields": {
            "product_object_id": {
                "$toObjectId": "$product_id",
            }
        }
    },
    {
        "$lookup": {
            "from": "products",
            "localField": "product_object_id",
            "foreignField": "_id",
            "as": "product",
        }
    },
    {
        "$unwind": "$product",
    },
    {
        "$group": {
            "_id": None,
            "inventory_value": {
                "$sum": {
                    "$multiply": [
                        "$current_stock",
                        "$product.purchase_price",
                    ]
                }
            },
        }
    },
]

        result = await cls.inventory_collection.aggregate(
            pipeline,
        ).to_list(1)

        if result:
            return result[0]["inventory_value"]

        return 0.0

    @classmethod
    async def get_category_distribution(cls):

        pipeline = [
    {
        "$addFields": {
            "product_object_id": {
                "$toObjectId": "$product_id",
            }
        }
    },
    {
        "$lookup": {
            "from": "products",
            "localField": "product_object_id",
            "foreignField": "_id",
            "as": "product",
        }
    },
    {
        "$unwind": "$product",
    },
    {
        "$group": {
            "_id": "$product.category",
            "units": {
                "$sum": "$current_stock",
            },
        }
    },
    {
        "$sort": {
            "_id": 1,
        }
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
                            }
                        },
                        "type": "$transaction_type",
                    },
                    "quantity": {
                        "$sum": "$quantity",
                    },
                }
            },
            {
                "$sort": {
                    "_id.date": 1,
                }
            },
        ]

        return await cls.transaction_collection.aggregate(
            pipeline,
        ).to_list(None)

    @classmethod
    async def get_inventory_value_last_10_days(cls):
        """
        Returns one point for each of the last 10 days.

        Since inventory only stores the latest stock quantity,
        the inventory value is the current inventory value repeated
        for each day. This satisfies the current project requirement.
        """

        current_value = await cls.get_inventory_value()

        today = datetime.utcnow().date()

        data = []

        for index in range(9, -1, -1):
            day = today - timedelta(days=index)

            data.append(
                {
                    "date": day.strftime("%Y-%m-%d"),
                    "revenue": current_value,
                }
            )

        return data