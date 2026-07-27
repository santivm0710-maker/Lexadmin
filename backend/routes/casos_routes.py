from fastapi import APIRouter

from backend.schemas.common import ApiResponse
from backend.schemas.requests import CasoCreate
from backend.services.caso_service import CasoService

router = APIRouter(prefix="/casos", tags=["casos"])
service = CasoService()


@router.get("/", response_model=ApiResponse)
def listar_casos():
    """Lista los casos almacenados en la base de datos."""
    return ApiResponse(
        success=True,
        message="Datos obtenidos correctamente.",
        data=service.listar(),
    )


@router.post("/", response_model=ApiResponse)
def crear_caso(caso: CasoCreate):
    """Crea un caso y lo guarda en la base de datos."""
    return ApiResponse(
        success=True,
        message="Caso creado correctamente.",
        data=service.crear(caso),
    )
