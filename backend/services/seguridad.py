"""Hash y verificación de contraseñas (PBKDF2-SHA256, stdlib puro)."""

import hashlib
import hmac
import secrets

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
