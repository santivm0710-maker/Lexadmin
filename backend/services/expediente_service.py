from backend.entities import Expediente
from backend.repositories.expediente_repository import ExpedienteRepository
from backend.schemas.requests import ExpedienteCreate


class ExpedienteService:
    def __init__(self):
        self.repository = ExpedienteRepository()

    def listar(self):
        return self.repository.list_all()

    def crear(self, datos: ExpedienteCreate) -> Expediente:
        return self.repository.add(Expediente(id_expediente=0, **datos.model_dump()))

    def actualizar(self, id_expediente: int, datos: ExpedienteCreate) -> Expediente | None:
        return self.repository.update(id_expediente, Expediente(id_expediente=id_expediente, **datos.model_dump()))

    def eliminar(self, id_expediente: int) -> bool:
        return self.repository.delete(id_expediente)
