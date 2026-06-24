from dataclasses import dataclass
from typing import Optional


@dataclass
class Expediente:
    id_expediente: int
    id_caso: int
    nombre_documento: str
    tipo_documento: str
    ruta_archivo: Optional[str] = None
    estado_ocr: str = "Pendiente"
