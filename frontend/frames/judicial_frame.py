import api_client as api
from crud_frame import CrudFrame
from ui_helpers import validar_email


class JudicialFrame(CrudFrame):
    recurso = "judicial"
    pk = "id_info_judicial"
    titulo = "Administración de Información Judicial"
    subtitulo = "Juzgado, juez, fiscal y contacto institucional asociados a cada caso."
    titulo_tabla = "Información judicial registrada"
    columnas = ("Caso", "Juzgado", "Juez", "Fiscal", "Contacto")
    columnas_form = 5
    texto_crear = "Guardar datos"
    texto_actualizar = "Actualizar datos"

    def definir_campos(self, form):
        self.campo(form, "caso", "Caso (expediente)", "Ej. #245", 0, 0)
        self.campo(form, "juzgado", "Juzgado", "Nombre del juzgado", 0, 1)
        self.campo(form, "juez", "Juez", "Nombre", 0, 2, tipo="texto")
        self.campo(form, "fiscal", "Fiscal", "Nombre", 0, 3, tipo="texto")
        self.campo(form, "contacto", "Contacto", "correo institucional", 0, 4)

    def refrescar(self):
        self._casos = {c["id_caso"]: c for c in api.listar("casos")}
        super().refrescar()

    def a_fila(self, r):
        caso = self._casos.get(r["id_caso"], {})
        return (caso.get("numero_expediente", "?"), r.get("juzgado") or "",
                r.get("juez") or "", r.get("fiscal") or "", r.get("contacto_institucional") or "")

    def validar(self, v):
        if not v["caso"] or not v["juzgado"]:
            return "El caso y el juzgado son obligatorios."
        if v["contacto"] and "@" in v["contacto"] and not validar_email(v["contacto"]):
            return "El contacto parece un correo, pero su formato no es válido."
        return None

    def a_cuerpo(self, v):
        caso = api.buscar_caso_por_expediente(v["caso"])
        if caso is None:
            raise ValueError(f"No existe un caso con expediente '{v['caso']}'.")
        return {
            "id_caso": caso["id_caso"],
            "juzgado": v["juzgado"],
            "juez": v["juez"] or None,
            "fiscal": v["fiscal"] or None,
            "contacto_institucional": v["contacto"] or None,
        }

    def llenar_formulario(self, r):
        caso = self._casos.get(r["id_caso"], {})
        self.poner("caso", caso.get("numero_expediente"))
        self.poner("juzgado", r.get("juzgado"))
        self.poner("juez", r.get("juez"))
        self.poner("fiscal", r.get("fiscal"))
        self.poner("contacto", r.get("contacto_institucional"))
