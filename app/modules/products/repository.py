from app.db.base_repository import BaseRepository
from app.db.database import database


class ProductRepository(BaseRepository):

    collection = database["products"]

    @classmethod
    async def get_product_by_sku(cls, sku: str):
        return await cls.find_one(
            {
                "sku": sku,
            }
        )