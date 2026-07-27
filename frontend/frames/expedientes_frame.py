import api_client as api
from crud_frame import CrudFrame
from ui_helpers import formatear_fecha


class ExpedientesFrame(CrudFrame):
    recurso = "expedientes"
    pk = "id_expediente"
    titulo = "Digitalización y Expedientes"
    subtitulo = "Documentos por caso, con su tipo y estado de digitalización (OCR)."
    titulo_tabla = "Documentos digitalizados"
    columnas = ("Cliente", "Caso", "Documento", "Tipo", "OCR", "Subido")
    columnas_form = 4
    texto_crear = "Subir documento"
    texto_actualizar = "Actualizar documento"

    def definir_campos(self, form):
        self.campo(form, "caso", "Caso (expediente)", "Ej. #245", 0, 0)
        self.campo(form, "nombre_documento", "Documento", "archivo.pdf", 0, 1)
        self.campo(form, "tipo_documento", "Tipo de documento", "Expediente / Prueba", 0, 2, tipo="texto")
        self.campo(form, "estado_ocr", "Estado OCR", "Pendiente / Procesado", 0, 3, tipo="texto")

    def refrescar(self):
        self._clientes = {c["id_cliente"]: c["nombre_completo"] for c in api.listar("clientes")}
        self._casos = {c["id_caso"]: c for c in api.listar("casos")}
        super().refrescar()

    def a_fila(self, r):
        caso = self._casos.get(r["id_caso"], {})
        return (self._clientes.get(r["id_cliente"], "?"), caso.get("numero_expediente", "?"),
                r.get("nombre_documento") or "", r.get("tipo_documento") or "",
                r.get("estado_ocr") or "", formatear_fecha(r.get("fecha_subida")))

    def validar(self, v):
        if not v["caso"] or not v["nombre_documento"] or not v["tipo_documento"]:
            return "Caso, documento y tipo son obligatorios."
        return None

    def a_cuerpo(self, v):
        caso = api.buscar_caso_por_expediente(v["caso"])
        if caso is None:
            raise ValueError(f"No existe un caso con expediente '{v['caso']}'. Créalo primero.")
        return {
            "id_cliente": caso["id_cliente"],
            "id_caso": caso["id_caso"],
            "nombre_documento": v["nombre_documento"],
            "tipo_documento": v["tipo_documento"],
            "estado_ocr": v["estado_ocr"] or "Pendiente",
        }

    def llenar_formulario(self, r):
        caso = self._casos.get(r["id_caso"], {})
        self.poner("caso", caso.get("numero_expediente"))
        self.poner("nombre_documento", r.get("nombre_documento"))
        self.poner("tipo_documento", r.get("tipo_documento"))
        self.poner("estado_ocr", r.get("estado_ocr"))
