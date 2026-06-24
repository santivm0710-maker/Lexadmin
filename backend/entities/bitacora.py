from dataclasses import dataclass
from datetime import datetime


@dataclass
class BitacoraEvento:
    id_evento: int
    fecha_hora: datetime
    actor: str
    modulo: str
    accion: str
    detalle: str
