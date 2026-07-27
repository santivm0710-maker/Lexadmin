from backend.entities import InformacionJudicial
from backend.repositories.judicial_repository import JudicialRepository
from backend.schemas.requests import JudicialCreate


class JudicialService:
    def __init__(self):
        self.repository = JudicialRepository()

    def listar(self):
        return self.repository.list_all()

    def crear(self, datos: JudicialCreate) -> InformacionJudicial:
        return self.repository.add(InformacionJudicial(id_info_judicial=0, **datos.model_dump()))
