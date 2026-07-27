from dataclasses import dataclass
from datetime import date, time, timedelta
from typing import Optional, Union


@dataclass
class BitacoraEvento:
    id_bitacora: int = 0
    fecha: Optional[date] = None
    hora: Optional[Union[time, timedelta, str]] = None
    actor: Optional[str] = None
    modulo: Optional[str] = None
    accion: Optional[str] = None
    descripcion: Optional[str] = None
