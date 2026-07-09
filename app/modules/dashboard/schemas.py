from datetime import datetime

from pydantic import BaseModel


class DashboardSummaryResponse(BaseModel):
    total_products: int
    total_suppliers: int
    total_purchase_orders: int
    pending_purchase_orders: int
    low_stock_items: int
    inventory_value: float


class InventoryCategoryData(BaseModel):
    category: str
    units: int


class RevenueProcurementData(BaseModel):
    date: datetime
    revenue: float
    procurement: float


class SalesCountData(BaseModel):
    date: datetime
    sales: int


class SalesByCustomerData(BaseModel):
    customer: str
    amount: float


class PurchaseOrderStatusData(BaseModel):
    status: str
    count: int


class MonthlyProcurementData(BaseModel):
    month: str
    amount: float


class DashboardChartsResponse(BaseModel):
    inventory_by_category: list[InventoryCategoryData]
    revenue_vs_procurement: list[RevenueProcurementData]
    sales_count: list[SalesCountData]
    sales_by_customer: list[SalesByCustomerData]
    purchase_order_status: list[PurchaseOrderStatusData]
    monthly_procurement: list[MonthlyProcurementData]


class RecentTransactionResponse(BaseModel):
    id: str
    product_id: str
    transaction_type: str
    quantity: int
    remarks: str
    created_by: str
    created_at: datetime


class RecentPurchaseOrderResponse(BaseModel):
    id: str
    po_number: str
    supplier_id: str
    status: str
    remarks: str | None
    created_by: str
    created_at: datetime


class RecentSaleResponse(BaseModel):
    id: str
    sale_number: str
    customer_name: str
    total_amount: float
    remarks: str | None
    created_by: str
    created_at: datetime


class DashboardRecentResponse(BaseModel):
    transactions: list[RecentTransactionResponse]
    purchase_orders: list[RecentPurchaseOrderResponse]
    sales: list[RecentSaleResponse]


class LowStockItemResponse(BaseModel):
    product_id: str
    current_stock: int
    reorder_level: int


class PendingPurchaseOrderResponse(BaseModel):
    id: str
    po_number: str
    supplier_id: str
    status: str
    created_by: str
    created_at: datetime


class DashboardAlertsResponse(BaseModel):
    low_stock: list[LowStockItemResponse]
    pending_purchase_orders: list[PendingPurchaseOrderResponse]