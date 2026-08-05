"""Dependencia de FastAPI para exigir sesión (JWT) en las rutas protegidas.

Uso en un router:

    from fastapi import APIRouter, Depends
    from backend.services.auth_dependency import obtener_usuario_actual

    router = APIRouter(prefix="/casos", dependencies=[Depends(obtener_usuario_actual)])

Con `dependencies=[...]` a nivel de router, FastAPI valida el token antes de
llegar a cualquier endpoint del router, sin tener que tocar la firma de cada
función. Si un endpoint necesita saber QUIÉN hizo la petición (para anotarlo
en la bitácora, por ejemplo), puede pedir el usuario directamente:

    def crear_caso(caso: CasoCreate, usuario: dict = Depends(obtener_usuario_actual)):
        ...
"""

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.services.seguridad import verificar_token

# auto_error=False para poder devolver nosotros un mensaje en español,
# en vez del genérico que da HTTPBearer cuando falta el header.
_esquema_bearer = HTTPBearer(auto_error=False)


def obtener_usuario_actual(
    credenciales: HTTPAuthorizationCredentials = Depends(_esquema_bearer),
) -> dict:
    """Valida el header `Authorization: Bearer <token>` y devuelve el payload
    del usuario (id_usuario, correo, nombre_completo, rol).

    Lanza 401 si falta el token, está mal formado, expiró o fue alterado.
    """
    if credenciales is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado. Inicia sesión de nuevo.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = verificar_token(credenciales.credentials)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="La sesión expiró. Inicia sesión de nuevo.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido. Inicia sesión de nuevo.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "id_usuario": int(payload["sub"]),
        "correo": payload.get("correo"),
        "nombre_completo": payload.get("nombre_completo"),
        "rol": payload.get("rol"),
    }