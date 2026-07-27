from fastapi import APIRouter, HTTPException

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


@router.put("/{id_expediente}", response_model=ApiResponse)
def actualizar_expediente(id_expediente: int, expediente: ExpedienteCreate):
    """Actualiza un expediente existente."""
    resultado = service.actualizar(id_expediente, expediente)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Expediente no encontrado.")
    return ApiResponse(success=True, message="Expediente actualizado correctamente.", data=resultado)


@router.delete("/{id_expediente}", response_model=ApiResponse)
def eliminar_expediente(id_expediente: int):
    """Elimina un expediente existente."""
    if not service.eliminar(id_expediente):
        raise HTTPException(status_code=404, detail="Expediente no encontrado.")
    return ApiResponse(success=True, message="Expediente eliminado correctamente.", data=None)
