from fastapi import APIRouter

from backend.schemas.common import ApiResponse
from backend.schemas.requests import JudicialCreate
from backend.services.judicial_service import JudicialService

router = APIRouter(prefix="/judicial", tags=["judicial"])
service = JudicialService()


@router.get("/", response_model=ApiResponse)
def listar_judicial():
    """Lista la información judicial almacenada en la base de datos."""
    return ApiResponse(
        success=True,
        message="Datos obtenidos correctamente.",
        data=service.listar(),
    )


@router.post("/", response_model=ApiResponse)
def crear_info_judicial(info: JudicialCreate):
    """Crea información judicial y la guarda en la base de datos."""
    return ApiResponse(
        success=True,
        message="Información judicial creada correctamente.",
        data=service.crear(info),
    )
