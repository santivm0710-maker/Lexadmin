from fastapi import APIRouter

from backend.schemas.common import ApiResponse
from backend.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])
service = DashboardService()


@router.get("/", response_model=ApiResponse)
def obtener_dashboard():
    """Indicadores del dashboard calculados en vivo desde la base de datos."""
    return ApiResponse(success=True, message="Dashboard obtenido correctamente.", data=service.resumen())
