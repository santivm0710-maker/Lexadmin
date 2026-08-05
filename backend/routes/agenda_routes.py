from fastapi import APIRouter, Depends, HTTPException

from backend.schemas.common import ApiResponse
from backend.schemas.requests import AgendaCreate
from backend.services.auth_dependency import obtener_usuario_actual
from backend.services.agenda_service import AgendaService

router = APIRouter(prefix="/agenda", tags=["agenda"], dependencies=[Depends(obtener_usuario_actual)])
service = AgendaService()


@router.get("/", response_model=ApiResponse)
def listar_agenda():
    return ApiResponse(success=True, message="Agenda obtenida correctamente.", data=service.listar())


@router.post("/", response_model=ApiResponse)
def crear_evento(evento: AgendaCreate):
    return ApiResponse(success=True, message="Evento creado correctamente.", data=service.crear(evento))


@router.put("/{id_agenda}", response_model=ApiResponse)
def actualizar_evento(id_agenda: int, evento: AgendaCreate):
    resultado = service.actualizar(id_agenda, evento)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado.")
    return ApiResponse(success=True, message="Evento actualizado correctamente.", data=resultado)


@router.delete("/{id_agenda}", response_model=ApiResponse)
def eliminar_evento(id_agenda: int):
    if not service.eliminar(id_agenda):
        raise HTTPException(status_code=404, detail="Evento no encontrado.")
    return ApiResponse(success=True, message="Evento eliminado correctamente.", data=None)
