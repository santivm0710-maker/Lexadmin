from fastapi import APIRouter

from backend.schemas.common import ApiResponse
from backend.schemas.requests import ExpedienteCreate
from backend.services.expediente_service import ExpedienteService

router = APIRouter(prefix="/expedientes", tags=["expedientes"])
service = ExpedienteService()


@router.get("/", response_model=ApiResponse)
def listar_expedientes():
    """Lista los expedientes almacenados en la base de datos."""
    return ApiResponse(
        success=True,
        message="Datos obtenidos correctamente.",
        data=service.listar(),
    )


@router.post("/", response_model=ApiResponse)
def crear_expediente(expediente: ExpedienteCreate):
    """Crea un expediente y lo guarda en la base de datos."""
    return ApiResponse(
        success=True,
        message="Expediente creado correctamente.",
        data=service.crear(expediente),
    )
