from fastapi import APIRouter

from backend.schemas.common import ApiResponse
from backend.services.judicial_service import JudicialService

router = APIRouter(prefix="/judicial", tags=["judicial"])
service = JudicialService()


@router.get("/", response_model=ApiResponse)
def listar_judicial():
    """Lista datos simulados del módulo judicial."""
    return ApiResponse(
        success=True,
        message="Datos simulados obtenidos correctamente.",
        data=service.listar(),
    )
