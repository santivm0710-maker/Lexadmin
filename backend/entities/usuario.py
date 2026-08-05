from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Usuario:
    id_usuario: int = 0
    nombre_completo: str = ""
    correo: str = ""
    password_hash: str = ""
    rol: str = "Abogado"
    fecha_registro: Optional[datetime] = None
