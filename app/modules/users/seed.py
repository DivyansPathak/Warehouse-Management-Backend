from app.db.database import database
from app.modules.auth.utils import hash_password


async def seed_admin():

    collection = database["users"]

    existing_admin = await collection.find_one(
        {
            "role": "admin",
        }
    )

    if existing_admin:
        print("Admin already exists.")
        return

    admin = {
        "name": "System Administrator",
        "email": "admin@warehouse.com",
        "password": hash_password("admin123"),
        "role": "admin",
        "is_active": True,
    }

    await collection.insert_one(admin)

    print("Admin created successfully.")