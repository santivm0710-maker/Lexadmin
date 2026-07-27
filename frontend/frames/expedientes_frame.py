import api_client as api
from crud_frame import CrudFrame
from ui_helpers import formatear_fecha

TIPOS_DOCUMENTO = ["Expediente", "Prueba", "Resolución", "Contrato", "Escrito", "Otro"]
ESTADOS_OCR = ["Pendiente", "Procesado"]


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
        self.desplegable(form, "caso", "Caso (expediente)", [], 0, 0, con_placeholder=True)
        self.campo(form, "nombre_documento", "Documento", "archivo.pdf", 0, 1)
        self.desplegable(form, "tipo_documento", "Tipo de documento", TIPOS_DOCUMENTO, 0, 2)
        self.desplegable(form, "estado_ocr", "Estado OCR", ESTADOS_OCR, 0, 3)

    def refrescar(self):
        self._clientes = {c["id_cliente"]: c["nombre_completo"] for c in api.listar("clientes")}
        self._casos = {c["id_caso"]: c for c in api.listar("casos")}
        self.opciones("caso", [c["numero_expediente"] for c in self._casos.values()])
        super().refrescar()

    def a_fila(self, r):
        caso = self._casos.get(r["id_caso"], {})
        return (self._clientes.get(r["id_cliente"], "?"), caso.get("numero_expediente", "?"),
                r.get("nombre_documento") or "", r.get("tipo_documento") or "",
                r.get("estado_ocr") or "", formatear_fecha(r.get("fecha_subida")))

    def validar(self, v):
        if not v["caso"]:
            return "Debes elegir un caso. Si no aparece, créalo primero en Casos."
        if not v["nombre_documento"]:
            return "El nombre del documento es obligatorio."
        return None

    def a_cuerpo(self, v):
        caso = api.buscar_caso_por_expediente(v["caso"])
        if caso is None:
            raise ValueError(f"No existe un caso con expediente '{v['caso']}'.")
        return {
            "id_cliente": caso["id_cliente"],
            "id_caso": caso["id_caso"],
            "nombre_documento": v["nombre_documento"],
            "tipo_documento": v["tipo_documento"] or None,
            "estado_ocr": v["estado_ocr"] or "Pendiente",
        }

    def llenar_formulario(self, r):
        caso = self._casos.get(r["id_caso"], {})
        self.poner("caso", caso.get("numero_expediente"))
        self.poner("nombre_documento", r.get("nombre_documento"))
        self.poner("tipo_documento", r.get("tipo_documento"))
        self.poner("estado_ocr", r.get("estado_ocr"))
