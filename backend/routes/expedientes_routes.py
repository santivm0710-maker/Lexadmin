from fastapi import APIRouter, Depends, HTTPException

from backend.schemas.common import ApiResponse
from backend.schemas.requests import ExpedienteCreate
from backend.services.auth_dependency import obtener_usuario_actual
from backend.services.expediente_service import ExpedienteService

router = APIRouter(prefix="/expedientes", tags=["expedientes"], dependencies=[Depends(obtener_usuario_actual)])
service = ExpedienteService()


@router.get("/", response_model=ApiResponse)
def listar_expedientes():
    return ApiResponse(success=True, message="Expedientes obtenidos correctamente.", data=service.listar())


@router.post("/", response_model=ApiResponse)
def crear_expediente(expediente: ExpedienteCreate):
    return ApiResponse(success=True, message="Expediente creado correctamente.", data=service.crear(expediente))


@router.put("/{id_expediente}", response_model=ApiResponse)
def actualizar_expediente(id_expediente: int, expediente: ExpedienteCreate):
    resultado = service.actualizar(id_expediente, expediente)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Expediente no encontrado.")
    return ApiResponse(success=True, message="Expediente actualizado correctamente.", data=resultado)


@router.delete("/{id_expediente}", response_model=ApiResponse)
def eliminar_expediente(id_expediente: int):
    if not service.eliminar(id_expediente):
        raise HTTPException(status_code=404, detail="Expediente no encontrado.")
    return ApiResponse(success=True, message="Expediente eliminado correctamente.", data=None)
