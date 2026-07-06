from app.modules.auth.utils import hash_password
from app.modules.users.models import AppUser
from app.modules.users.repository import UserRepository
from app.utils.mongo import serialize_document, serialize_documents


class UserService:

    @staticmethod
    async def create_user(request):

        existing = await UserRepository.find_by_email(
            request.email,
        )

        if existing:
            raise ValueError(
                "User already exists",
            )

        user = AppUser(
            name=request.name,
            email=request.email,
            password=hash_password(request.password),
            role=request.role,
        )

        result = await UserRepository.create(
            user.model_dump(),
        )

        return str(result.inserted_id)

    @staticmethod
    async def get_all_users():

        users = await UserRepository.get_all()

        return serialize_documents(users)

    @staticmethod
    async def get_user_by_id(user_id: str):

        user = await UserRepository.get_by_id(
            user_id,
        )

        return serialize_document(user)

    @staticmethod
    async def update_user(
        user_id: str,
        request,
    ):
        await UserRepository.update(
            user_id,
            request.model_dump(),
        )

    @staticmethod
    async def delete_user(user_id: str):
        await UserRepository.delete(
            user_id,
        )