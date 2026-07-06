from app.db.base_repository import BaseRepository
from app.db.database import database


class SupplierRepository(BaseRepository):

    collection = database["suppliers"]

    @classmethod
    async def get_supplier_by_email(cls, email: str):
        return await cls.find_one(
            {
                "email": email,
            }
        )