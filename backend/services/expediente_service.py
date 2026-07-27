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
