import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from backend.services.expediente_service import ExpedienteService

"Pruebas para la funcionalidad de subida de archivos PDF en el servicio de expedientes."
class ExpedienteServiceUploadTests(unittest.TestCase):
    def test_guarda_pdf_en_directorio_de_uploads(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            origen = tmp_path / "documento.pdf"
            origen.write_bytes(b"%PDF-1.4\n%mock")

            service = ExpedienteService()
            destino = service._guardar_archivo_pdf(
                str(origen),
                id_caso=7,
                nombre_documento="Contrato",
                base_dir=tmp_path / "uploads",
            )

            self.assertIsInstance(destino, str)
            self.assertTrue(Path(destino).exists())
            self.assertTrue(Path(destino).name.endswith(".pdf"))
            self.assertEqual(Path(destino).suffix.lower(), ".pdf")
            "El archivo se ha guardado correctamente en el directorio de uploads."
    def test_usa_directorio_externo_si_esta_configurado(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            with patch.dict(os.environ, {"LEXADMIN_UPLOADS_DIR": str(tmp_path)}):
                service = ExpedienteService()
                carpeta = service._resolver_dir_uploads(id_caso=99)

            self.assertEqual(carpeta, tmp_path / "expedientes" / "99")


if __name__ == "__main__":
    unittest.main()
