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

    def actualizar(self, id_evento: int, datos: BitacoraCreate) -> BitacoraEvento | None:
        return self.repository.update(id_evento, BitacoraEvento(id_evento=id_evento, **datos.model_dump()))

    def eliminar(self, id_evento: int) -> bool:
        return self.repository.delete(id_evento)
