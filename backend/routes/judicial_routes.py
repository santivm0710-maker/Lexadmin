from fastapi import APIRouter, Depends, HTTPException

from backend.schemas.common import ApiResponse
from backend.schemas.requests import JudicialCreate
from backend.services.auth_dependency import obtener_usuario_actual
from backend.services.judicial_service import JudicialService

router = APIRouter(prefix="/judicial", tags=["judicial"], dependencies=[Depends(obtener_usuario_actual)])
service = JudicialService()


@router.get("/", response_model=ApiResponse)
def listar_judicial():
    return ApiResponse(success=True, message="Información judicial obtenida correctamente.", data=service.listar())


@router.post("/", response_model=ApiResponse)
def crear_info_judicial(info: JudicialCreate):
    return ApiResponse(success=True, message="Información judicial creada correctamente.", data=service.crear(info))


@router.put("/{id_info}", response_model=ApiResponse)
def actualizar_info_judicial(id_info: int, info: JudicialCreate):
    resultado = service.actualizar(id_info, info)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Información judicial no encontrada.")
    return ApiResponse(success=True, message="Información judicial actualizada correctamente.", data=resultado)


@router.delete("/{id_info}", response_model=ApiResponse)
def eliminar_info_judicial(id_info: int):
    if not service.eliminar(id_info):
        raise HTTPException(status_code=404, detail="Información judicial no encontrada.")
    return ApiResponse(success=True, message="Información judicial eliminada correctamente.", data=None)
