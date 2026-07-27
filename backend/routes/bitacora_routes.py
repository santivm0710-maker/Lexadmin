from fastapi import APIRouter

from backend.schemas.common import ApiResponse
from backend.services.bitacora_service import BitacoraService

router = APIRouter(prefix="/bitacora", tags=["bitacora"])
service = BitacoraService()


@router.get("/", response_model=ApiResponse)
def listar_bitacora():
    """La bitácora es solo de lectura; se llena automáticamente."""
    return ApiResponse(success=True, message="Bitácora obtenida correctamente.", data=service.listar())
