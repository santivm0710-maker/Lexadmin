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


def _post(endpoint: str, payload: dict):
    """Envía datos a un endpoint del backend. Devuelve (exito, mensaje, data)."""
    url = f"{API_BASE_URL}{endpoint}"
    cuerpo = json.dumps(payload).encode("utf-8")
    request = Request(
        url,
        data=cuerpo,
        method="POST",
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )

    try:
        with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            respuesta = json.loads(response.read().decode("utf-8"))
            return True, respuesta.get("message", "Operación exitosa."), respuesta.get("data")
    except HTTPError as error:
        try:
            detalle = json.loads(error.read().decode("utf-8"))
            mensaje = detalle.get("detail", str(detalle))
        except (json.JSONDecodeError, OSError):
            mensaje = f"Error HTTP {error.code}."
        return False, mensaje, None
    except (URLError, TimeoutError, OSError):
        return False, "No se pudo conectar con el backend. Verifica que esté corriendo.", None


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

    clientes = _get("/clientes/") or []
    nombres_por_id = {item.get("id_cliente"): item.get("nombre", "") for item in clientes}
    return [
        (
            item.get("numero_expediente", ""),
            nombres_por_id.get(item.get("id_cliente"), f"Cliente ID {item.get('id_cliente', '')}"),
            item.get("tipo_caso", ""),
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
            item.get("nombre_documento", ""),
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


def crear_cliente(nombre, cedula, telefono="", correo="", caso_relacionado=None):
    return _post(
        "/clientes/",
        {
            "nombre": nombre,
            "cedula": cedula,
            "telefono": telefono or None,
            "correo": correo or None,
            "caso_relacionado": caso_relacionado,
        },
    )


def crear_caso(numero_expediente, id_cliente, tipo_caso, estado, prioridad, abogado_responsable=None):
    return _post(
        "/casos/",
        {
            "numero_expediente": numero_expediente,
            "id_cliente": id_cliente,
            "tipo_caso": tipo_caso,
            "estado": estado,
            "prioridad": prioridad,
            "abogado_responsable": abogado_responsable or None,
        },
    )


def crear_expediente(id_caso, nombre_documento, tipo_documento, ruta_archivo=None, estado_ocr="Pendiente"):
    return _post(
        "/expedientes/",
        {
            "id_caso": id_caso,
            "nombre_documento": nombre_documento,
            "tipo_documento": tipo_documento,
            "ruta_archivo": ruta_archivo or None,
            "estado_ocr": estado_ocr,
        },
    )


def crear_evento_agenda(id_caso, fecha, hora, actividad, lugar, prioridad):
    return _post(
        "/agenda/",
        {
            "id_caso": id_caso,
            "fecha": fecha,
            "hora": hora,
            "actividad": actividad,
            "lugar": lugar,
            "prioridad": prioridad,
        },
    )


def crear_info_judicial(id_caso, juzgado, juez=None, fiscal=None, contacto_institucional=None):
    return _post(
        "/judicial/",
        {
            "id_caso": id_caso,
            "juzgado": juzgado,
            "juez": juez or None,
            "fiscal": fiscal or None,
            "contacto_institucional": contacto_institucional or None,
        },
    )


def buscar_id_cliente_por_nombre(nombre: str):
    data = _get("/clientes/") or []
    nombre = nombre.strip().lower()
    for item in data:
        if item.get("nombre", "").strip().lower() == nombre:
            return item.get("id_cliente")
    return None


def buscar_id_caso_por_expediente(numero_expediente: str):
    data = _get("/casos/") or []
    numero_expediente = numero_expediente.strip()
    if numero_expediente and not numero_expediente.startswith("#"):
        numero_expediente = f"#{numero_expediente}"
    numero_expediente = numero_expediente.lower()
    for item in data:
        if item.get("numero_expediente", "").strip().lower() == numero_expediente:
            return item.get("id_caso")
    return None


def _formatear_fecha_hora(valor: str) -> str:
    try:
        fecha = datetime.fromisoformat(valor)
        return fecha.strftime("%d/%m/%Y %H:%M")
    except ValueError:
        return valor
