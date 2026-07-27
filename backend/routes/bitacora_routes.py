from fastapi import APIRouter

from backend.schemas.common import ApiResponse
from backend.schemas.requests import BitacoraCreate
from backend.services.bitacora_service import BitacoraService

router = APIRouter(prefix="/bitacora", tags=["bitacora"])
service = BitacoraService()


@router.get("/", response_model=ApiResponse)
def listar_bitacora():
    """Lista los eventos de bitácora almacenados en la base de datos."""
    return ApiResponse(
        success=True,
        message="Datos obtenidos correctamente.",
        data=service.listar(),
    )


@router.post("/", response_model=ApiResponse)
def crear_evento_bitacora(evento: BitacoraCreate):
    """Crea un evento de bitácora y lo guarda en la base de datos."""
    return ApiResponse(
        success=True,
        message="Evento de bitácora creado correctamente.",
        data=service.crear(evento),
    )
