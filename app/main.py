from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.db.database import client
from app.modules.auth.router import router as auth_router
from app.modules.inventory.router import router as inventory_router
from app.modules.products.router import router as product_router
from app.modules.suppliers.router import router as supplier_router
from app.modules.users.router import router as user_router
from app.modules.users.seed import seed_admin
from app.modules.purchase_orders.router import router as purchase_order_router
from app.modules.dashboard.router import router as dashboard_router
from app.modules.sales.router import router as sales_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("MongoDB Connected")

    await seed_admin()

    yield

    client.close()

    print("MongoDB Connection Closed")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(product_router)
app.include_router(supplier_router)
app.include_router(inventory_router)
app.include_router(purchase_order_router)
app.include_router(dashboard_router)
app.include_router(sales_router)

@app.get("/")
async def root():
    return {
        "message": settings.app_name,
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
    }