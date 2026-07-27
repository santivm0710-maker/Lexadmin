from backend.entities import Caso
from backend.repositories.caso_repository import CasoRepository
from backend.schemas.requests import CasoCreate
from backend.services import auditoria

MODULO = "Casos"


class CasoService:
    def __init__(self):
        self.repository = CasoRepository()

    def listar(self):
        return self.repository.list_all()

    def crear(self, datos: CasoCreate) -> Caso:
        caso = self.repository.add(Caso(**datos.model_dump()))
        auditoria.registrar(MODULO, "Creación", f"Se creó el caso {caso.numero_expediente}.")
        return caso

    def actualizar(self, id_caso: int, datos: CasoCreate) -> "Caso | None":
        caso = self.repository.update(id_caso, Caso(id_caso=id_caso, **datos.model_dump()))
        if caso is not None:
            auditoria.registrar(MODULO, "Actualización", f"Se actualizó el caso {caso.numero_expediente}.")
        return caso

    def eliminar(self, id_caso: int) -> bool:
        eliminado = self.repository.delete(id_caso)
        if eliminado:
            auditoria.registrar(MODULO, "Eliminación", f"Se eliminó el caso con ID {id_caso}.")
        return eliminado
