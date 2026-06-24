from fastapi import APIRouter

from backend.schemas.common import ApiResponse
from backend.services.bitacora_service import BitacoraService

router = APIRouter(prefix="/bitacora", tags=["bitacora"])
service = BitacoraService()


@router.get("/", response_model=ApiResponse)
def listar_bitacora():
    """Lista datos simulados del módulo bitacora."""
    return ApiResponse(
        success=True,
        message="Datos simulados obtenidos correctamente.",
        data=service.listar(),
    )
