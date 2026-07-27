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

    def actualizar(self, id_info_judicial: int, datos: JudicialCreate) -> InformacionJudicial | None:
        return self.repository.update(
            id_info_judicial, InformacionJudicial(id_info_judicial=id_info_judicial, **datos.model_dump())
        )

    def eliminar(self, id_info_judicial: int) -> bool:
        return self.repository.delete(id_info_judicial)
