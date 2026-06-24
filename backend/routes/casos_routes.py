from fastapi import APIRouter

from backend.schemas.common import ApiResponse
from backend.services.caso_service import CasoService

router = APIRouter(prefix="/casos", tags=["casos"])
service = CasoService()


@router.get("/", response_model=ApiResponse)
def listar_casos():
    """Lista datos simulados del módulo casos."""
    return ApiResponse(
        success=True,
        message="Datos simulados obtenidos correctamente.",
        data=service.listar(),
    )
