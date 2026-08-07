"""Cliente HTTP hacia el backend FastAPI de LexAdmin.

Expone funciones genéricas (listar/crear/actualizar/eliminar) que sirven
para cualquier módulo, más ayudantes para el dashboard, los reportes y la
búsqueda de identificadores por nombre o expediente.
"""

from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API_BASE_URL = "http://127.0.0.1:8000"
TIMEOUT = 4

# Token de la sesión activa. Se guarda en memoria del proceso (la app es de
# un solo usuario a la vez); lo llena `iniciar sesion` y lo vacía
# `cerrar sesion`. Todas las peticiones lo adjuntan automáticamente, así que
# el resto del frontend (frames, crud_frame, etc.) no tiene que preocuparse
# por él: siguen llamando a listar/crear/actualizar/eliminar como siempre.

_token = None

def cerrar_sesion():
    """Olvida el token actual. Llamarlo al cerrar sesión o si expiró."""
    global _token
    _token = None

def _pedir(endpoint, metodo="GET", cuerpo=None):
    """Realiza una petición y devuelve (ok, mensaje, data)."""
    datos = json.dumps(cuerpo).encode("utf-8") if cuerpo is not None else None
    cabeceras = {"Accept": "application/json"}
    if datos is not None:
        cabeceras["Content-Type"] = "application/json"
    if _token:
        cabeceras["Authorization"] = f"Bearer {_token}"
    peticion = Request(f"{API_BASE_URL}{endpoint}", data=datos, method=metodo, headers=cabeceras)

    try:
        with urlopen(peticion, timeout=TIMEOUT) as respuesta:
            payload = json.loads(respuesta.read().decode("utf-8"))
            return True, payload.get("message", ""), payload.get("data")
    except HTTPError as error:
        try:
            detalle = json.loads(error.read().decode("utf-8")).get("detail", "")
        except (json.JSONDecodeError, OSError):
            detalle = f"Error HTTP {error.code}."
        if error.code == 401:
            # El token venció o es inválido: no tiene sentido seguir
            # mandándolo, así que se limpia para que quede claro que hay
            # que volver a iniciar sesión.
            cerrar_sesion()
            detalle = detalle or "Tu sesión expiró. Inicia sesión de nuevo."
        return False, detalle, None
    except (URLError, TimeoutError, OSError):
        return False, "No se pudo conectar con el backend. Verifica que esté corriendo.", None


def _pedir_multipart(endpoint, metodo="POST", cuerpo=None, archivo_path=None):
    """Envía un formulario multipart para subir un PDF junto con los datos del expediente."""
    boundary = f"----LexAdminBoundary{uuid4().hex}"
    partes = []

    for clave, valor in (cuerpo or {}).items():
        if valor is None:
            continue
        partes.append(f"--{boundary}\r\n".encode("utf-8"))
        partes.append(f'Content-Disposition: form-data; name="{clave}"\r\n\r\n'.encode("utf-8"))
        partes.append(f"{valor}\r\n".encode("utf-8"))

    if archivo_path:
        archivo = Path(archivo_path)
        if archivo.exists():
            partes.append(f"--{boundary}\r\n".encode("utf-8"))
            partes.append(f'Content-Disposition: form-data; name="archivo"; filename="{archivo.name}"\r\n'.encode("utf-8"))
            partes.append(b"Content-Type: application/pdf\r\n\r\n")
            partes.append(archivo.read_bytes())
            partes.append(b"\r\n")

    partes.append(f"--{boundary}--\r\n".encode("utf-8"))
    datos = b"".join(partes)
    cabeceras = {
    "Accept": "application/json",
    "Content-Type": f"multipart/form-data; boundary={boundary}",
}
    "Recibe el token de sesión si hay uno activo y lo adjunta a la cabecera Authorization."
    if _token:
        cabeceras["Authorization"] = f"Bearer {_token}"

    "realiza la petición HTTP al backend y devuelve (ok, mensaje, data)."
    peticion = Request(
    f"{API_BASE_URL}{endpoint}",
    data=datos,
    method=metodo,
    headers=cabeceras,
)

    try:
        with urlopen(peticion, timeout=TIMEOUT) as respuesta:
            payload = json.loads(respuesta.read().decode("utf-8"))
            return True, payload.get("message", ""), payload.get("data")
    except HTTPError as error:
        try:
            detalle = json.loads(error.read().decode("utf-8")).get("detail", "")
        except (json.JSONDecodeError, OSError):
            detalle = f"Error HTTP {error.code}."
        return False, detalle, None
    except (URLError, TimeoutError, OSError):
        return False, "No se pudo conectar con el backend. Verifica que esté corriendo.", None


# ------------------------------------------------------------------
# CRUD genérico (recurso = 'clientes', 'casos', 'agenda', ...)
# ------------------------------------------------------------------
def listar(recurso):
    _, _, data = _pedir(f"/{recurso}/")
    return data or []


def crear(recurso, cuerpo):
    return _pedir(f"/{recurso}/", "POST", cuerpo)


def crear_con_archivo(recurso, cuerpo, archivo_path=None):
    """Crea un registro enviando datos + archivo PDF en una sola petición."""
    return _pedir_multipart(f"/{recurso}/", "POST", cuerpo, archivo_path)


def actualizar(recurso, item_id, cuerpo):
    return _pedir(f"/{recurso}/{item_id}", "PUT", cuerpo)


def actualizar_con_archivo(recurso, item_id, cuerpo, archivo_path=None):
    """Actualiza un registro enviando datos + archivo PDF en una sola petición."""
    return _pedir_multipart(f"/{recurso}/{item_id}", "PUT", cuerpo, archivo_path)


def eliminar(recurso, item_id):
    return _pedir(f"/{recurso}/{item_id}", "DELETE")


# ------------------------------------------------------------------
# Autenticación
# ------------------------------------------------------------------
def registrar_usuario(cuerpo):
    return _pedir("/usuarios/registro", "POST", cuerpo)


def iniciar_sesion(cuerpo):
    global _token
    ok, mensaje, data = _pedir("/usuarios/login", "POST", cuerpo)
    if ok and data:
        _token = data.get("token")
    return ok, mensaje, data


# ------------------------------------------------------------------
# Consultas de apoyo
# ------------------------------------------------------------------
def backend_disponible():
    ok, _, _ = _pedir("/conexion")
    return ok


def obtener_dashboard():
    _, _, data = _pedir("/dashboard/")
    return data or {"stats": [], "casos_atencion": [], "actividad_reciente": []}


def obtener_reportes():
    _, _, data = _pedir("/reportes/")
    return data or {"indicadores": [], "resumen": []}


def buscar_cliente_por_nombre(nombre):
    nombre = nombre.strip().lower()
    for cliente in listar("clientes"):
        if cliente.get("nombre_completo", "").strip().lower() == nombre:
            return cliente
    return None


def buscar_caso_por_expediente(expediente):
    expediente = expediente.strip().lstrip("#").lower()
    for caso in listar("casos"):
        if caso.get("numero_expediente", "").strip().lstrip("#").lower() == expediente:
            return caso
    return None
