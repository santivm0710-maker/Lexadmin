from fastapi import APIRouter, HTTPException

from backend.schemas.common import ApiResponse
from backend.schemas.requests import UsuarioLogin, UsuarioRegistro
from backend.services.usuario_service import UsuarioService

router = APIRouter(prefix="/usuarios", tags=["usuarios"])
service = UsuarioService()


def _publico(usuario):
    return {
        "id_usuario": usuario.id_usuario,
        "nombre_completo": usuario.nombre_completo,
        "correo": usuario.correo,
        "rol": usuario.rol,
    }


@router.post("/registro", response_model=ApiResponse)
def registrar_usuario(datos: UsuarioRegistro):
    usuario = service.registrar(datos)
    return ApiResponse(success=True, message="Cuenta creada correctamente.", data=_publico(usuario))


@router.post("/login", response_model=ApiResponse)
def iniciar_sesion(datos: UsuarioLogin):
    usuario = service.login(datos)
    if usuario is None:
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos.")
    return ApiResponse(success=True, message="Sesión iniciada correctamente.", data=_publico(usuario))
