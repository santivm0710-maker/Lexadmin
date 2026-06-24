from dataclasses import dataclass
from typing import Optional


@dataclass
class InformacionJudicial:
    id_info_judicial: int
    id_caso: int
    juzgado: str
    juez: Optional[str]
    fiscal: Optional[str]
    contacto_institucional: Optional[str]
