from fastapi import APIRouter

from backend.schemas.common import ApiResponse
from backend.services.reportes_service import ReportesService

router = APIRouter(prefix="/reportes", tags=["reportes"])
service = ReportesService()


@router.get("/", response_model=ApiResponse)
def obtener_reportes():
    """Indicadores y resumen calculados en vivo desde la base de datos."""
    return ApiResponse(success=True, message="Reportes obtenidos correctamente.", data=service.resumen())
