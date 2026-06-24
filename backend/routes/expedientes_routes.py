from fastapi import APIRouter

from backend.schemas.common import ApiResponse
from backend.services.expediente_service import ExpedienteService

router = APIRouter(prefix="/expedientes", tags=["expedientes"])
service = ExpedienteService()


@router.get("/", response_model=ApiResponse)
def listar_expedientes():
    """Lista datos simulados del módulo expedientes."""
    return ApiResponse(
        success=True,
        message="Datos simulados obtenidos correctamente.",
        data=service.listar(),
    )
