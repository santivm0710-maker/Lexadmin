from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Cliente:
    id_cliente: int = 0
    nombre_completo: str = ""
    identificacion: str = ""
    telefono: Optional[str] = None
    correo: Optional[str] = None
    fecha_registro: Optional[datetime] = None
