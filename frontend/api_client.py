"""Cliente API prototipo para conectar el frontend con el backend FastAPI.

Este archivo NO conecta a una base de datos. Solo consume los endpoints
simulados del backend cuando están disponibles. Si el backend no está
corriendo, el frontend usa los datos locales de `data.py` como respaldo.
"""

from __future__ import annotations

import json
from datetime import datetime
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen

try:
    import data as fallback_data
except ModuleNotFoundError:
    from frontend import data as fallback_data

API_BASE_URL = "http://127.0.0.1:8000"
TIMEOUT_SECONDS = 2


def _get(endpoint: str):
    """Consulta un endpoint del backend y devuelve el campo data."""
    url = f"{API_BASE_URL}{endpoint}"
    request = Request(url, headers={"Accept": "application/json"})

    try:
        with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            payload = json.loads(response.read().decode("utf-8"))
            return payload.get("data", [])
    except (URLError, HTTPError, TimeoutError, json.JSONDecodeError, OSError):
        return None


def backend_disponible() -> bool:
    return _get("/conexion") is not None


def obtener_clientes():
    data = _get("/clientes/")
    if data is None:
        return fallback_data.CLIENTES
    return [
        (
            item.get("nombre", ""),
            item.get("cedula", ""),
            item.get("telefono", ""),
            item.get("correo", ""),
            item.get("caso_relacionado", ""),
        )
        for item in data
    ]


def obtener_casos():
    data = _get("/casos/")
    if data is None:
        return fallback_data.CASOS

    clientes = {item[4]: item[0] for item in obtener_clientes()}
    return [
        (
            item.get("numero_expediente", ""),
            clientes.get(f"Caso {item.get('numero_expediente', '')}", f"Cliente ID {item.get('id_cliente', '')}"),
            item.get("tipo_proceso", ""),
            item.get("estado", ""),
            item.get("prioridad", ""),
            item.get("abogado_responsable", ""),
        )
        for item in data
    ]


def obtener_expedientes():
    data = _get("/expedientes/")
    if data is None:
        return fallback_data.EXPEDIENTES

    casos = _get("/casos/") or []
    casos_por_id = {item.get("id_caso"): item.get("numero_expediente") for item in casos}
    return [
        (
            f"Caso ID {item.get('id_caso', '')}",
            casos_por_id.get(item.get("id_caso"), ""),
            item.get("nombre_archivo", ""),
            item.get("tipo_documento", ""),
            item.get("estado_ocr", ""),
            "Cliente/Caso/Documento",
        )
        for item in data
    ]


def obtener_agenda():
    data = _get("/agenda/")
    if data is None:
        return fallback_data.AGENDA

    casos = _get("/casos/") or []
    casos_por_id = {item.get("id_caso"): item.get("numero_expediente") for item in casos}
    return [
        (
            item.get("fecha", ""),
            item.get("hora", ""),
            casos_por_id.get(item.get("id_caso"), f"Caso ID {item.get('id_caso', '')}"),
            item.get("actividad", ""),
            item.get("lugar", ""),
            item.get("prioridad", ""),
        )
        for item in data
    ]


def obtener_judicial():
    data = _get("/judicial/")
    if data is None:
        return fallback_data.JUDICIAL

    casos = _get("/casos/") or []
    casos_por_id = {item.get("id_caso"): item.get("numero_expediente") for item in casos}
    return [
        (
            casos_por_id.get(item.get("id_caso"), f"Caso ID {item.get('id_caso', '')}"),
            item.get("juzgado", ""),
            item.get("juez", ""),
            item.get("fiscal", "") or "No registrado",
            item.get("contacto_institucional", ""),
        )
        for item in data
    ]


def obtener_bitacora():
    data = _get("/bitacora/")
    if data is None:
        return fallback_data.BITACORA

    return [
        (
            _formatear_fecha_hora(item.get("fecha_hora", "")),
            item.get("actor", ""),
            item.get("modulo", ""),
            item.get("accion", ""),
            item.get("detalle", ""),
        )
        for item in data
    ]


def obtener_dashboard_stats():
    data = _get("/dashboard/")
    if data is None:
        return fallback_data.DASHBOARD_STATS
    return [tuple(item) for item in data.get("stats", fallback_data.DASHBOARD_STATS)]


def obtener_casos_atencion():
    data = _get("/dashboard/")
    if data is None:
        return fallback_data.CASOS_ATENCION
    return [tuple(item) for item in data.get("casos_atencion", fallback_data.CASOS_ATENCION)]


def obtener_actividad_reciente():
    data = _get("/dashboard/")
    if data is None:
        return fallback_data.ACTIVIDAD_RECIENTE
    return [tuple(item) for item in data.get("actividad_reciente", fallback_data.ACTIVIDAD_RECIENTE)]


def obtener_reportes():
    data = _get("/reportes/")
    if data is None:
        return fallback_data.REPORTES
    return [tuple(item) for item in data.get("resumen", fallback_data.REPORTES)]


def obtener_indicadores_reportes():
    data = _get("/reportes/")
    if data is None:
        return None
    return [tuple(item) for item in data.get("indicadores", [])]


def _formatear_fecha_hora(valor: str) -> str:
    try:
        fecha = datetime.fromisoformat(valor)
        return fecha.strftime("%d/%m/%Y %H:%M")
    except ValueError:
        return valor
