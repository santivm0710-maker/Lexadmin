from fastapi import APIRouter, HTTPException

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


@router.put("/{id_cliente}", response_model=ApiResponse)
def actualizar_cliente(id_cliente: int, cliente: ClienteCreate):
    """Actualiza un cliente existente."""
    resultado = service.actualizar(id_cliente, cliente)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado.")
    return ApiResponse(success=True, message="Cliente actualizado correctamente.", data=resultado)


@router.delete("/{id_cliente}", response_model=ApiResponse)
def eliminar_cliente(id_cliente: int):
    """Elimina un cliente existente."""
    if not service.eliminar(id_cliente):
        raise HTTPException(status_code=404, detail="Cliente no encontrado.")
    return ApiResponse(success=True, message="Cliente eliminado correctamente.", data=None)
