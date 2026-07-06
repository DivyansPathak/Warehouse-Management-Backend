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


class RevenueOrdersData(BaseModel):
    date: str
    revenue: float
    orders: int


class DashboardChartsResponse(BaseModel):
    inventory_by_category: list[InventoryCategoryData]
    revenue_vs_orders: list[RevenueOrdersData]


class RecentTransactionResponse(BaseModel):
    id: str
    product_id: str
    transaction_type: str
    quantity: int
    remarks: str
    created_by: str
    created_at: str


class RecentPurchaseOrderResponse(BaseModel):
    id: str
    po_number: str
    supplier_id: str
    status: str
    remarks: str | None
    created_by: str
    created_at: str


class DashboardRecentResponse(BaseModel):
    transactions: list[RecentTransactionResponse]
    purchase_orders: list[RecentPurchaseOrderResponse]


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
    created_at: str


class DashboardAlertsResponse(BaseModel):
    low_stock: list[LowStockItemResponse]
    pending_purchase_orders: list[PendingPurchaseOrderResponse]