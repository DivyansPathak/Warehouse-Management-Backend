from bson import ObjectId


class BaseRepository:

    collection = None

    @classmethod
    async def create(cls, data: dict):
        return await cls.collection.insert_one(data)

    @classmethod
    async def get_all(cls):
        return await cls.collection.find().to_list(None)

    @classmethod
    async def get_by_id(cls, document_id: str):
        return await cls.collection.find_one(
            {
                "_id": ObjectId(document_id),
            }
        )

    @classmethod
    async def update(
        cls,
        document_id: str,
        data: dict,
    ):
        return await cls.collection.update_one(
            {
                "_id": ObjectId(document_id),
            },
            {
                "$set": data,
            },
        )

    @classmethod
    async def delete(cls, document_id: str):
        return await cls.collection.delete_one(
            {
                "_id": ObjectId(document_id),
            }
        )

    @classmethod
    async def count(cls):
        return await cls.collection.count_documents({})

    @classmethod
    async def find_one(cls, query: dict):
        return await cls.collection.find_one(query)

    @classmethod
    async def exists(cls, query: dict):
        return await cls.collection.find_one(query) is not None