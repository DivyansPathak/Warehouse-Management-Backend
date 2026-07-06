from app.core.security import create_access_token
from app.modules.auth.models import User
from app.modules.auth.repository import AuthRepository
from app.modules.auth.utils import hash_password, verify_password


class AuthService:

    @staticmethod
    async def register(name: str, email: str, password: str):

        existing_user = await AuthRepository.find_by_email(email)

        if existing_user:
            raise ValueError("User already exists")

        user = User(
            name=name,
            email=email,
            password=hash_password(password),
        )

        result = await AuthRepository.create_user(
            user.model_dump()
        )

        return str(result.inserted_id)

    @staticmethod
    async def login(email: str, password: str):

        user = await AuthRepository.find_by_email(email)

        if not user:
            raise ValueError("Invalid email or password")

        if not verify_password(password, user["password"]):
            raise ValueError("Invalid email or password")

        access_token = create_access_token(
            {
                "sub": str(user["_id"]),
                "email": user["email"],
                "role": user["role"],
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }