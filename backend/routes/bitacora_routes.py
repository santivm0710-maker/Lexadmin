from fastapi import APIRouter, HTTPException

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


@router.put("/{id_evento}", response_model=ApiResponse)
def actualizar_evento_bitacora(id_evento: int, evento: BitacoraCreate):
    """Actualiza un evento de bitácora existente."""
    resultado = service.actualizar(id_evento, evento)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado.")
    return ApiResponse(success=True, message="Evento de bitácora actualizado correctamente.", data=resultado)


@router.delete("/{id_evento}", response_model=ApiResponse)
def eliminar_evento_bitacora(id_evento: int):
    """Elimina un evento de bitácora existente."""
    if not service.eliminar(id_evento):
        raise HTTPException(status_code=404, detail="Evento no encontrado.")
    return ApiResponse(success=True, message="Evento de bitácora eliminado correctamente.", data=None)
