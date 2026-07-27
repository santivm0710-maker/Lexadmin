"""Cliente HTTP hacia el backend FastAPI de LexAdmin.

Expone funciones genéricas (listar/crear/actualizar/eliminar) que sirven
para cualquier módulo, más ayudantes para el dashboard, los reportes y la
búsqueda de identificadores por nombre o expediente.
"""

from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API_BASE_URL = "http://127.0.0.1:8000"
TIMEOUT = 4


def _pedir(endpoint, metodo="GET", cuerpo=None):
    """Realiza una petición y devuelve (ok, mensaje, data)."""
    datos = json.dumps(cuerpo).encode("utf-8") if cuerpo is not None else None
    cabeceras = {"Accept": "application/json"}
    if datos is not None:
        cabeceras["Content-Type"] = "application/json"
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


def actualizar(recurso, item_id, cuerpo):
    return _pedir(f"/{recurso}/{item_id}", "PUT", cuerpo)


def eliminar(recurso, item_id):
    return _pedir(f"/{recurso}/{item_id}", "DELETE")


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
