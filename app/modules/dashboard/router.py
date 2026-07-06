from fastapi import APIRouter

from app.modules.dashboard.schemas import (
    DashboardAlertsResponse,
    DashboardChartsResponse,
    DashboardRecentResponse,
    DashboardSummaryResponse,
)
from app.modules.dashboard.service import DashboardService

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "",
    response_model=DashboardSummaryResponse,
)
async def get_dashboard():
    return await DashboardService.get_dashboard()


@router.get(
    "/charts",
    response_model=DashboardChartsResponse,
)
async def get_dashboard_charts():
    return await DashboardService.get_charts()


@router.get(
    "/recent",
    response_model=DashboardRecentResponse,
)
async def get_recent_activity():
    return await DashboardService.get_recent()


@router.get(
    "/alerts",
    response_model=DashboardAlertsResponse,
)
async def get_dashboard_alerts():
    return await DashboardService.get_alerts()