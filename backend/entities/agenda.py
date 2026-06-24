from dataclasses import dataclass
from datetime import date, time


@dataclass
class EventoAgenda:
    id_evento: int
    id_caso: int
    fecha: date
    hora: time
    actividad: str
    lugar: str
    prioridad: str
