"""Registro automático en la bitácora.

Los servicios llaman a `registrar(...)` después de crear, actualizar o
eliminar información. Así la bitácora se llena sola con la actividad real
del sistema, sin datos inventados.
"""

from datetime import datetime

from backend.entities import BitacoraEvento
from backend.repositories.bitacora_repository import BitacoraRepository

_repositorio = BitacoraRepository()


def registrar(modulo, accion, descripcion, actor="Usuario"):
    ahora = datetime.now()
    evento = BitacoraEvento(
        fecha=ahora.date(),
        hora=ahora.strftime("%H:%M:%S"),
        actor=actor,
        modulo=modulo,
        accion=accion,
        descripcion=descripcion,
    )
    try:
        _repositorio.add(evento)
    except Exception:
        # El registro de auditoría nunca debe interrumpir la operación real.
        pass
