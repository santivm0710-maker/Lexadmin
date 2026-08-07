import os
import re
import shutil
from pathlib import Path
from typing import Optional

from backend.entities import Expediente
from backend.repositories.caso_repository import CasoRepository
from backend.repositories.expediente_repository import ExpedienteRepository
from backend.schemas.requests import ExpedienteCreate
from backend.services import auditoria

MODULO = "Expedientes"


class ExpedienteService:
    def __init__(self):
        self.repository = ExpedienteRepository()
        self.caso_repository = CasoRepository()

    def listar(self):
        return self.repository.list_all()

    def _slugify(self, texto: Optional[str]) -> str:
        """Convierte un nombre de archivo en un texto seguro para guardar en disco."""
        texto = re.sub(r"[^A-Za-z0-9]+", "-", texto or "documento").strip("-").lower()
        return texto or "documento"

    def _obtener_numero_expediente(self, id_caso: int) -> str:
        caso = self.caso_repository.get_by_id(id_caso)
        return caso.numero_expediente if caso and caso.numero_expediente else str(id_caso)

    def _resolver_dir_uploads(
        self,
        *,
        id_caso: int,
        numero_expediente: Optional[str] = None,
        base_dir: Optional[Path] = None,
    ) -> Path:
        """Determina la carpeta donde se almacenarán los PDFs del expediente."""
        carpeta_caso = numero_expediente or self._obtener_numero_expediente(id_caso)
        carpeta_caso = self._slugify(carpeta_caso)

        if base_dir is not None:
            return base_dir / "expedientes" / carpeta_caso

        env_dir = os.getenv("LEXADMIN_UPLOADS_DIR")
        if env_dir:
            return Path(env_dir).expanduser().resolve() / "expedientes" / carpeta_caso

        escritorio = Path.home() / "OneDrive" / "Escritorio" / "Uploads"
        return escritorio / "expedientes" / carpeta_caso

    def _guardar_archivo_pdf(
        self,
        archivo_path: Optional[str],
        *,
        id_caso: int,
        numero_expediente: Optional[str] = None,
        nombre_documento: Optional[str],
        base_dir: Optional[Path] = None,
    ) -> Optional[str]:
        """Copia un archivo PDF a la carpeta de uploads y devuelve la ruta guardada."""
        if not archivo_path:
            return None

        origen = Path(archivo_path)
        if not origen.exists():
            raise FileNotFoundError(f"No se encontró el archivo: {archivo_path}")
        if origen.suffix.lower() != ".pdf":
            raise ValueError("Solo se permiten archivos PDF.")

        carpeta = self._resolver_dir_uploads(
            id_caso=id_caso,
            numero_expediente=numero_expediente,
            base_dir=base_dir,
        )
        carpeta.mkdir(parents=True, exist_ok=True)

        base_name = self._slugify(nombre_documento or origen.stem)
        destino = carpeta / f"{base_name}.pdf"
        contador = 1
        while destino.exists():
            destino = carpeta / f"{base_name}_{contador}.pdf"
            contador += 1

        shutil.copy2(origen, destino)
        return str(destino)

    def crear(self, datos: ExpedienteCreate, archivo_pdf: Optional[str] = None) -> Expediente:
        """Crea un expediente y, si viene un PDF, lo guarda y registra su ruta."""
        datos_dict = datos.model_dump(exclude_unset=True)
        if archivo_pdf:
            ruta_pdf = self._guardar_archivo_pdf(
                archivo_pdf,
                id_caso=datos_dict.get("id_caso") or 0,
                numero_expediente=self._obtener_numero_expediente(datos_dict.get("id_caso") or 0),
                nombre_documento=datos_dict.get("nombre_documento"),
            )
            if ruta_pdf:
                datos_dict["ruta_pdf"] = ruta_pdf

        exp = self.repository.add(Expediente(**datos_dict))
        auditoria.registrar(MODULO, "Creación", f"Se subió el documento {exp.nombre_documento}.")
        return exp

    def actualizar(self, id_expediente: int, datos: ExpedienteCreate, archivo_pdf: Optional[str] = None) -> "Expediente | None":
        """Actualiza un expediente y reemplaza el PDF si se envía uno nuevo."""
        datos_dict = datos.model_dump(exclude_unset=True)
        if archivo_pdf:
            ruta_pdf = self._guardar_archivo_pdf(
                archivo_pdf,
                id_caso=datos_dict.get("id_caso") or 0,
                numero_expediente=self._obtener_numero_expediente(datos_dict.get("id_caso") or 0),
                nombre_documento=datos_dict.get("nombre_documento"),
            )
            if ruta_pdf:
                datos_dict["ruta_pdf"] = ruta_pdf

        exp = self.repository.update(id_expediente, Expediente(id_expediente=id_expediente, **datos_dict))
        if exp is not None:
            auditoria.registrar(MODULO, "Actualización", f"Se actualizó el documento {exp.nombre_documento}.")
        return exp

    def eliminar(self, id_expediente: int) -> bool:
        expediente = self.repository.get_by_id(id_expediente)
        ruta_pdf = expediente.ruta_pdf if expediente else None
        eliminado = self.repository.delete(id_expediente)
        if eliminado:
            if ruta_pdf and Path(ruta_pdf).exists():
                try:
                    Path(ruta_pdf).unlink()
                except OSError:
                    pass
            auditoria.registrar(MODULO, "Eliminación", f"Se eliminó el expediente con ID {id_expediente}.")
        return eliminado
