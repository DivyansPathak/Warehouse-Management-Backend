from app.modules.suppliers.models import Supplier
from app.modules.suppliers.repository import SupplierRepository
from app.utils.mongo import serialize_document, serialize_documents


class SupplierService:

    @staticmethod
    async def create_supplier(request):

        existing = await SupplierRepository.get_supplier_by_email(
            request.email,
        )

        if existing:
            raise ValueError(
                "Supplier already exists",
            )

        supplier = Supplier(
            **request.model_dump(),
        )

        result = await SupplierRepository.create(
            supplier.model_dump(),
        )

        return str(result.inserted_id)

    @staticmethod
    async def get_all_suppliers():

        suppliers = await SupplierRepository.get_all()

        return serialize_documents(
            suppliers,
        )

    @staticmethod
    async def get_supplier_by_id(
        supplier_id: str,
    ):

        supplier = await SupplierRepository.get_by_id(
            supplier_id,
        )

        return serialize_document(
            supplier,
        )

    @staticmethod
    async def update_supplier(
        supplier_id: str,
        request,
    ):
        await SupplierRepository.update(
            supplier_id,
            request.model_dump(),
        )

    @staticmethod
    async def delete_supplier(
        supplier_id: str,
    ):
        await SupplierRepository.delete(
            supplier_id,
        )