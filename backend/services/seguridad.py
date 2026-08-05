"""Hash y verificación de contraseñas (PBKDF2-SHA256, stdlib puro) y
manejo de tokens JWT para la sesión del usuario.
"""

import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone

import jwt

from backend.config import settings

_ITERACIONES = 100_000


def hash_password(password: str) -> str:
    sal = secrets.token_hex(16)
    hash_ = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(sal), _ITERACIONES)
    return f"{sal}${hash_.hex()}"


def verificar_password(password: str, password_hash: str) -> bool:
    try:
        sal, hash_guardado = password_hash.split("$", 1)
    except ValueError:
        return False
    hash_calculado = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), bytes.fromhex(sal), _ITERACIONES
    ).hex()
    return hmac.compare_digest(hash_calculado, hash_guardado)


# ----------------------------------------------------------------------
# JWT: se emite uno al iniciar sesión y se exige en el resto de la API.
# ----------------------------------------------------------------------
def crear_token(usuario) -> str:
    """Genera un JWT firmado con los datos públicos del usuario."""
    ahora = datetime.now(timezone.utc)
    payload = {
        "sub": str(usuario.id_usuario),
        "correo": usuario.correo,
        "nombre_completo": usuario.nombre_completo,
        "rol": usuario.rol,
        "iat": ahora,
        "exp": ahora + timedelta(minutes=settings.jwt_expiration_minutos),
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def verificar_token(token: str) -> dict:
    """Decodifica y valida un JWT. Lanza jwt.PyJWTError si no es válido."""
    return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])