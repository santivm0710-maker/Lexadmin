from fastapi import APIRouter

from backend.schemas.common import ApiResponse
from backend.services.agenda_service import AgendaService

router = APIRouter(prefix="/agenda", tags=["agenda"])
service = AgendaService()


@router.get("/", response_model=ApiResponse)
def listar_agenda():
    """Lista datos simulados del módulo agenda."""
    return ApiResponse(
        success=True,
        message="Datos simulados obtenidos correctamente.",
        data=service.listar(),
    )
