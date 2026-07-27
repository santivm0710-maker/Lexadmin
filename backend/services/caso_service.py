from backend.entities import Caso
from backend.repositories.caso_repository import CasoRepository
from backend.schemas.requests import CasoCreate


class CasoService:
    def __init__(self):
        self.repository = CasoRepository()

    def listar(self):
        return self.repository.list_all()

    def crear(self, datos: CasoCreate) -> Caso:
        return self.repository.add(Caso(id_caso=0, **datos.model_dump()))

    def actualizar(self, id_caso: int, datos: CasoCreate) -> Caso | None:
        return self.repository.update(id_caso, Caso(id_caso=id_caso, **datos.model_dump()))

    def eliminar(self, id_caso: int) -> bool:
        return self.repository.delete(id_caso)
