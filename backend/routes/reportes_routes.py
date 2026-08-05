from fastapi import APIRouter, Depends

from backend.schemas.common import ApiResponse
from backend.services.reportes_service import ReportesService
from backend.services.auth_dependency import obtener_usuario_actual

router = APIRouter(prefix="/reportes", tags=["reportes"], dependencies=[Depends(obtener_usuario_actual)])
service = ReportesService()


@router.get("/", response_model=ApiResponse)
def obtener_reportes():
    """Indicadores y resumen calculados en vivo desde la base de datos."""
    return ApiResponse(success=True, message="Reportes obtenidos correctamente.", data=service.resumen())
