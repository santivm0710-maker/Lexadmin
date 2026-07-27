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
