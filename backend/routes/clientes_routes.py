from fastapi import APIRouter

from backend.schemas.common import ApiResponse
from backend.schemas.requests import ClienteCreate
from backend.services.cliente_service import ClienteService

router = APIRouter(prefix="/clientes", tags=["clientes"])
service = ClienteService()


@router.get("/", response_model=ApiResponse)
def listar_clientes():
    """Lista los clientes almacenados en la base de datos."""
    return ApiResponse(
        success=True,
        message="Datos obtenidos correctamente.",
        data=service.listar(),
    )


@router.post("/", response_model=ApiResponse)
def crear_cliente(cliente: ClienteCreate):
    """Crea un cliente y lo guarda en la base de datos."""
    return ApiResponse(
        success=True,
        message="Cliente creado correctamente.",
        data=service.crear(cliente),
    )
