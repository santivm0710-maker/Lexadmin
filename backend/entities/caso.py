from dataclasses import dataclass
from typing import Optional


@dataclass
class Caso:
    id_caso: int
    numero_expediente: str
    id_cliente: int
    tipo_caso: str
    estado: str
    prioridad: str
    abogado_responsable: Optional[str] = None
