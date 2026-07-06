from app.db.database import database


class AuthRepository:

    collection = database["users"]

    @classmethod
    async def find_by_email(cls, email: str):
        return await cls.collection.find_one({"email": email})

    @classmethod
    async def create_user(cls, user: dict):
        return await cls.collection.insert_one(user)