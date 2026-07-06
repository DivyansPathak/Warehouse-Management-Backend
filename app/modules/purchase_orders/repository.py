from app.db.base_repository import BaseRepository
from app.db.database import database


class PurchaseOrderRepository(BaseRepository):

    collection = database["purchase_orders"]

    @classmethod
    async def get_pending_count(cls):
        return await cls.collection.count_documents(
            {
                "status": "PENDING",
            }
        )

    @classmethod
    async def get_status_summary(cls):

        pipeline = [
            {
                "$group": {
                    "_id": "$status",
                    "count": {
                        "$sum": 1,
                    },
                },
            },
        ]

        return await cls.collection.aggregate(
            pipeline,
        ).to_list(None)

    @classmethod
    async def get_monthly_procurement(cls):

        pipeline = [
            {
                "$unwind": "$items",
            },
            {
                "$group": {
                    "_id": {
                        "$dateToString": {
                            "format": "%Y-%m",
                            "date": "$created_at",
                        },
                    },
                    "amount": {
                        "$sum": {
                            "$multiply": [
                                "$items.purchase_price",
                                "$items.quantity",
                            ],
                        },
                    },
                },
            },
            {
                "$sort": {
                    "_id": 1,
                },
            },
        ]

        return await cls.collection.aggregate(
            pipeline,
        ).to_list(None)