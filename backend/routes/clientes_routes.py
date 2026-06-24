from fastapi import APIRouter

from backend.schemas.common import ApiResponse
from backend.services.cliente_service import ClienteService

router = APIRouter(prefix="/clientes", tags=["clientes"])
service = ClienteService()


@router.get("/", response_model=ApiResponse)
def listar_clientes():
    """Lista datos simulados del módulo clientes."""
    return ApiResponse(
        success=True,
        message="Datos simulados obtenidos correctamente.",
        data=service.listar(),
    )
