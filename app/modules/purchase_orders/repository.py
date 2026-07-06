from datetime import datetime, timedelta

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
    async def get_pending(cls):
        return await cls.collection.find(
            {
                "status": "PENDING",
            }
        ).sort(
            "created_at",
            -1,
        ).to_list(None)

    @classmethod
    async def get_recent(
        cls,
        limit: int = 10,
    ):
        return await cls.collection.find().sort(
            "created_at",
            -1,
        ).limit(limit).to_list(limit)

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

    @classmethod
    async def get_orders_last_10_days(cls):
        """
        Returns purchase order counts for each of the last 10 days.
        """

        start_date = datetime.utcnow() - timedelta(days=9)

        pipeline = [
            {
                "$match": {
                    "created_at": {
                        "$gte": start_date,
                    }
                }
            },
            {
                "$group": {
                    "_id": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$created_at",
                        }
                    },
                    "orders": {
                        "$sum": 1,
                    },
                }
            },
            {
                "$sort": {
                    "_id": 1,
                }
            },
        ]

        results = await cls.collection.aggregate(
            pipeline,
        ).to_list(None)

        order_map = {
            item["_id"]: item["orders"]
            for item in results
        }

        today = datetime.utcnow().date()

        data = []

        for index in range(9, -1, -1):
            day = today - timedelta(days=index)
            date = day.strftime("%Y-%m-%d")

            data.append(
                {
                    "date": date,
                    "orders": order_map.get(date, 0),
                }
            )

        return data