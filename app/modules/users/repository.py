from app.db.base_repository import BaseRepository
from app.db.database import database


class UserRepository(BaseRepository):

    collection = database["users"]

    @classmethod
    async def find_by_email(cls, email: str):
        return await cls.find_one(
            {
                "email": email,
            }
        )