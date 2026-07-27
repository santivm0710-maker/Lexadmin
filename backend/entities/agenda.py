from dataclasses import dataclass
from datetime import date, time, timedelta
from typing import Optional, Union


@dataclass
class EventoAgenda:
    id_agenda: int = 0
    id_caso: int = 0
    fecha: Optional[date] = None
    # MySQL devuelve las columnas TIME como timedelta; aceptamos ambos.
    hora: Optional[Union[time, timedelta, str]] = None
    actividad: Optional[str] = None
    lugar: Optional[str] = None
    prioridad: Optional[str] = None
    observaciones: Optional[str] = None
