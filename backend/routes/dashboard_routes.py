from fastapi import APIRouter, Depends

from backend.schemas.common import ApiResponse
from backend.services.dashboard_service import DashboardService
from backend.services.auth_dependency import obtener_usuario_actual

router = APIRouter(prefix="/dashboard", tags=["dashboard"], dependencies=[Depends(obtener_usuario_actual)])
service = DashboardService()


@router.get("/", response_model=ApiResponse)
def obtener_dashboard():
    """Indicadores del dashboard calculados en vivo desde la base de datos."""
    return ApiResponse(success=True, message="Dashboard obtenido correctamente.", data=service.resumen())
