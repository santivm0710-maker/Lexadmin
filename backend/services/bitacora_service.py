from backend.entities import BitacoraEvento
from backend.repositories.bitacora_repository import BitacoraRepository
from backend.schemas.requests import BitacoraCreate


class BitacoraService:
    def __init__(self):
        self.repository = BitacoraRepository()

    def listar(self):
        return self.repository.list_all()

    def crear(self, datos: BitacoraCreate) -> BitacoraEvento:
        return self.repository.add(BitacoraEvento(id_evento=0, **datos.model_dump()))
