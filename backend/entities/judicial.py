from dataclasses import dataclass
from typing import Optional


@dataclass
class InformacionJudicial:
    id_info_judicial: int = 0
    id_caso: int = 0
    juzgado: Optional[str] = None
    juez: Optional[str] = None
    fiscal: Optional[str] = None
    contacto_institucional: Optional[str] = None
