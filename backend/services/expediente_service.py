from backend.entities import Expediente
from backend.repositories.expediente_repository import ExpedienteRepository
from backend.schemas.requests import ExpedienteCreate
from backend.services import auditoria

MODULO = "Expedientes"


class ExpedienteService:
    def __init__(self):
        self.repository = ExpedienteRepository()

    def listar(self):
        return self.repository.list_all()

    def crear(self, datos: ExpedienteCreate) -> Expediente:
        exp = self.repository.add(Expediente(**datos.model_dump()))
        auditoria.registrar(MODULO, "Creación", f"Se subió el documento {exp.nombre_documento}.")
        return exp

    def actualizar(self, id_expediente: int, datos: ExpedienteCreate) -> "Expediente | None":
        exp = self.repository.update(id_expediente, Expediente(id_expediente=id_expediente, **datos.model_dump()))
        if exp is not None:
            auditoria.registrar(MODULO, "Actualización", f"Se actualizó el documento {exp.nombre_documento}.")
        return exp

    def eliminar(self, id_expediente: int) -> bool:
        eliminado = self.repository.delete(id_expediente)
        if eliminado:
            auditoria.registrar(MODULO, "Eliminación", f"Se eliminó el expediente con ID {id_expediente}.")
        return eliminado
