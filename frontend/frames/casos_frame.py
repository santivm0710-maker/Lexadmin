import api_client as api
from crud_frame import CrudFrame


class CasosFrame(CrudFrame):
    recurso = "casos"
    pk = "id_caso"
    titulo = "Gestión de Casos Legales"
    subtitulo = "Creación, actualización y seguimiento de expedientes jurídicos."
    titulo_tabla = "Casos registrados"
    columnas = ("Expediente", "Cliente", "Tipo de proceso", "Estado", "Prioridad", "Responsable")
    columnas_form = 3
    texto_crear = "Crear caso"
    texto_actualizar = "Actualizar caso"

    def definir_campos(self, form):
        self.campo(form, "cliente", "Cliente asociado", "Nombre exacto del cliente", 0, 0, tipo="texto")
        self.campo(form, "numero_expediente", "N.º expediente", "Ej. #245", 0, 1)
        self.campo(form, "tipo_proceso", "Tipo de proceso", "Civil, laboral, familia...", 0, 2, tipo="texto")
        self.campo(form, "estado", "Estado", "Activo / En revisión", 1, 0, tipo="texto")
        self.campo(form, "prioridad", "Prioridad", "Alta / Media / Urgente", 1, 1, tipo="texto")
        self.campo(form, "abogado_responsable", "Abogado responsable", "Lic. responsable", 1, 2, tipo="texto")

    def refrescar(self):
        self._clientes = {c["id_cliente"]: c["nombre_completo"] for c in api.listar("clientes")}
        super().refrescar()

    def a_fila(self, r):
        return (r["numero_expediente"], self._clientes.get(r["id_cliente"], "?"),
                r.get("tipo_proceso") or "", r.get("estado") or "",
                r.get("prioridad") or "", r.get("abogado_responsable") or "")

    def validar(self, v):
        obligatorios = (v["cliente"], v["numero_expediente"], v["tipo_proceso"], v["estado"], v["prioridad"])
        if not all(obligatorios):
            return "Cliente, expediente, tipo, estado y prioridad son obligatorios."
        return None

    def a_cuerpo(self, v):
        cliente = api.buscar_cliente_por_nombre(v["cliente"])
        if cliente is None:
            raise ValueError(f"No existe un cliente llamado '{v['cliente']}'. Regístralo primero.")
        return {
            "id_cliente": cliente["id_cliente"],
            "numero_expediente": v["numero_expediente"],
            "tipo_proceso": v["tipo_proceso"],
            "estado": v["estado"],
            "prioridad": v["prioridad"],
            "abogado_responsable": v["abogado_responsable"] or None,
        }

    def llenar_formulario(self, r):
        self.poner("cliente", self._clientes.get(r["id_cliente"], ""))
        self.poner("numero_expediente", r.get("numero_expediente"))
        self.poner("tipo_proceso", r.get("tipo_proceso"))
        self.poner("estado", r.get("estado"))
        self.poner("prioridad", r.get("prioridad"))
        self.poner("abogado_responsable", r.get("abogado_responsable"))
