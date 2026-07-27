from backend.entities import InformacionJudicial
from backend.repositories.judicial_repository import JudicialRepository
from backend.schemas.requests import JudicialCreate
from backend.services import auditoria

MODULO = "Información judicial"


class JudicialService:
    def __init__(self):
        self.repository = JudicialRepository()

    def listar(self):
        return self.repository.list_all()

    def crear(self, datos: JudicialCreate) -> InformacionJudicial:
        info = self.repository.add(InformacionJudicial(**datos.model_dump()))
        auditoria.registrar(MODULO, "Creación", f"Se registró información judicial del caso ID {info.id_caso}.")
        return info

    def actualizar(self, id_info: int, datos: JudicialCreate) -> "InformacionJudicial | None":
        info = self.repository.update(id_info, InformacionJudicial(id_info_judicial=id_info, **datos.model_dump()))
        if info is not None:
            auditoria.registrar(MODULO, "Actualización", f"Se actualizó información judicial del caso ID {info.id_caso}.")
        return info

    def eliminar(self, id_info: int) -> bool:
        eliminado = self.repository.delete(id_info)
        if eliminado:
            auditoria.registrar(MODULO, "Eliminación", f"Se eliminó información judicial con ID {id_info}.")
        return eliminado
