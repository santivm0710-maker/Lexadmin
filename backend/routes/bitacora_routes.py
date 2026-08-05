from fastapi import APIRouter, Depends

from backend.schemas.common import ApiResponse
from backend.services.bitacora_service import BitacoraService
from backend.services.auth_dependency import obtener_usuario_actual

router = APIRouter(prefix="/bitacora", tags=["bitacora"], dependencies=[Depends(obtener_usuario_actual)])
service = BitacoraService()


@router.get("/", response_model=ApiResponse)
def listar_bitacora():
    """La bitácora es solo de lectura; se llena automáticamente."""
    return ApiResponse(success=True, message="Bitácora obtenida correctamente.", data=service.listar())
