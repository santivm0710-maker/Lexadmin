from fastapi import APIRouter, HTTPException

from backend.schemas.common import ApiResponse
from backend.schemas.requests import AgendaCreate
from backend.services.agenda_service import AgendaService

router = APIRouter(prefix="/agenda", tags=["agenda"])
service = AgendaService()


@router.get("/", response_model=ApiResponse)
def listar_agenda():
    """Lista los eventos de agenda almacenados en la base de datos."""
    return ApiResponse(
        success=True,
        message="Datos obtenidos correctamente.",
        data=service.listar(),
    )


@router.post("/", response_model=ApiResponse)
def crear_evento(evento: AgendaCreate):
    """Crea un evento de agenda y lo guarda en la base de datos."""
    return ApiResponse(
        success=True,
        message="Evento creado correctamente.",
        data=service.crear(evento),
    )


@router.put("/{id_evento}", response_model=ApiResponse)
def actualizar_evento(id_evento: int, evento: AgendaCreate):
    """Actualiza un evento de agenda existente."""
    resultado = service.actualizar(id_evento, evento)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado.")
    return ApiResponse(success=True, message="Evento actualizado correctamente.", data=resultado)


@router.delete("/{id_evento}", response_model=ApiResponse)
def eliminar_evento(id_evento: int):
    """Elimina un evento de agenda existente."""
    if not service.eliminar(id_evento):
        raise HTTPException(status_code=404, detail="Evento no encontrado.")
    return ApiResponse(success=True, message="Evento eliminado correctamente.", data=None)
