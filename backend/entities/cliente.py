from dataclasses import dataclass
from typing import Optional


@dataclass
class Cliente:
    id_cliente: int
    nombre: str
    cedula: str
    telefono: str
    correo: str
    caso_relacionado: Optional[str] = None
