from fastapi import APIRouter, HTTPException

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


@router.put("/{id_info_judicial}", response_model=ApiResponse)
def actualizar_info_judicial(id_info_judicial: int, info: JudicialCreate):
    """Actualiza información judicial existente."""
    resultado = service.actualizar(id_info_judicial, info)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Información judicial no encontrada.")
    return ApiResponse(success=True, message="Información judicial actualizada correctamente.", data=resultado)


@router.delete("/{id_info_judicial}", response_model=ApiResponse)
def eliminar_info_judicial(id_info_judicial: int):
    """Elimina información judicial existente."""
    if not service.eliminar(id_info_judicial):
        raise HTTPException(status_code=404, detail="Información judicial no encontrada.")
    return ApiResponse(success=True, message="Información judicial eliminada correctamente.", data=None)
