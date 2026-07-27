from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Expediente:
    id_expediente: int = 0
    id_cliente: int = 0
    id_caso: int = 0
    nombre_documento: Optional[str] = None
    tipo_documento: Optional[str] = None
    ruta_pdf: Optional[str] = None
    estado_ocr: Optional[str] = "Pendiente"
    fecha_subida: Optional[datetime] = None
