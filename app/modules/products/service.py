from app.modules.products.models import Product
from app.modules.products.repository import ProductRepository
from app.utils.mongo import serialize_document, serialize_documents


class ProductService:

    @staticmethod
    async def create_product(request):

        existing = await ProductRepository.get_product_by_sku(
            request.sku,
        )

        if existing:
            raise ValueError("SKU already exists")

        product = Product(
            **request.model_dump(),
        )

        result = await ProductRepository.create(
            product.model_dump(),
        )

        return str(result.inserted_id)

    @staticmethod
    async def get_all_products():

        products = await ProductRepository.get_all()

        return serialize_documents(products)

    @staticmethod
    async def get_product_by_id(product_id: str):

        product = await ProductRepository.get_by_id(
            product_id,
        )

        return serialize_document(product)

    @staticmethod
    async def update_product(
        product_id: str,
        request,
    ):
        await ProductRepository.update(
            product_id,
            request.model_dump(),
        )

    @staticmethod
    async def delete_product(product_id: str):
        await ProductRepository.delete(
            product_id,
        )