from fastapi import APIRouter, HTTPException

from backend.schemas.common import ApiResponse
from backend.schemas.requests import CasoCreate
from backend.services.caso_service import CasoService

router = APIRouter(prefix="/casos", tags=["casos"])
service = CasoService()


@router.get("/", response_model=ApiResponse)
def listar_casos():
    return ApiResponse(success=True, message="Casos obtenidos correctamente.", data=service.listar())


@router.post("/", response_model=ApiResponse)
def crear_caso(caso: CasoCreate):
    return ApiResponse(success=True, message="Caso creado correctamente.", data=service.crear(caso))


@router.put("/{id_caso}", response_model=ApiResponse)
def actualizar_caso(id_caso: int, caso: CasoCreate):
    resultado = service.actualizar(id_caso, caso)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Caso no encontrado.")
    return ApiResponse(success=True, message="Caso actualizado correctamente.", data=resultado)


@router.delete("/{id_caso}", response_model=ApiResponse)
def eliminar_caso(id_caso: int):
    if not service.eliminar(id_caso):
        raise HTTPException(status_code=404, detail="Caso no encontrado.")
    return ApiResponse(success=True, message="Caso eliminado correctamente.", data=None)
