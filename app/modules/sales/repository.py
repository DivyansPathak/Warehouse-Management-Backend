from datetime import datetime, timedelta, time

from app.db.base_repository import BaseRepository
from app.db.database import database


class SalesRepository(BaseRepository):

    collection = database["sales"]

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
    async def get_sales_count_last_10_days(cls):

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
                    "sales": {
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

        data_map = {
            item["_id"]: item["sales"]
            for item in results
        }

        today = datetime.utcnow().date()

        data = []

        for index in range(9, -1, -1):

            day = today - timedelta(days=index)

            date_key = day.strftime("%Y-%m-%d")

            data.append(
                {
                    "date": datetime.combine(
                        day,
                        time.min,
                    ).isoformat(),
                    "sales": data_map.get(
                        date_key,
                        0,
                    ),
                }
            )

        return data

    @classmethod
    async def get_sales_by_customer(cls):

        pipeline = [
            {
                "$group": {
                    "_id": "$customer_name",
                    "amount": {
                        "$sum": "$total_amount",
                    },
                }
            },
            {
                "$sort": {
                    "amount": -1,
                }
            },
        ]

        results = await cls.collection.aggregate(
            pipeline,
        ).to_list(None)

        return [
            {
                "customer": item["_id"],
                "amount": round(
                    item["amount"],
                    2,
                ),
            }
            for item in results
        ]

    @classmethod
    async def get_revenue_vs_procurement_last_10_days(
        cls,
    ):

        start_date = datetime.utcnow() - timedelta(days=9)

        sales_pipeline = [
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
                    "revenue": {
                        "$sum": "$total_amount",
                    },
                }
            },
        ]

        sales_results = await cls.collection.aggregate(
            sales_pipeline,
        ).to_list(None)

        revenue_map = {
            item["_id"]: item["revenue"]
            for item in sales_results
        }

        purchase_collection = database["purchase_orders"]

        procurement_pipeline = [
            {
                "$match": {
                    "created_at": {
                        "$gte": start_date,
                    }
                }
            },
            {
                "$unwind": "$items",
            },
            {
                "$group": {
                    "_id": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$created_at",
                        }
                    },
                    "procurement": {
                        "$sum": {
                            "$multiply": [
                                "$items.purchase_price",
                                "$items.quantity",
                            ]
                        }
                    },
                }
            },
        ]

        procurement_results = (
            await purchase_collection.aggregate(
                procurement_pipeline,
            ).to_list(None)
        )

        procurement_map = {
            item["_id"]: item["procurement"]
            for item in procurement_results
        }

        today = datetime.utcnow().date()

        data = []

        for index in range(9, -1, -1):

            day = today - timedelta(days=index)

            date_key = day.strftime("%Y-%m-%d")

            data.append(
                {
                    "date": datetime.combine(
                        day,
                        time.min,
                    ).isoformat(),
                    "revenue": round(
                        revenue_map.get(
                            date_key,
                            0.0,
                        ),
                        2,
                    ),
                    "procurement": round(
                        procurement_map.get(
                            date_key,
                            0.0,
                        ),
                        2,
                    ),
                }
            )

        return data