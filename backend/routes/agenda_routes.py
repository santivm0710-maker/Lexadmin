from fastapi import APIRouter

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
