from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Caso:
    id_caso: int = 0
    id_cliente: int = 0
    numero_expediente: str = ""
    tipo_proceso: Optional[str] = None
    estado: Optional[str] = None
    prioridad: Optional[str] = None
    abogado_responsable: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_cierre: Optional[date] = None
