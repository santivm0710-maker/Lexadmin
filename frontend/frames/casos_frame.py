import api_client as api
from crud_frame import CrudFrame

TIPOS_PROCESO = ["Civil", "Laboral", "Familia", "Penal", "Administrativo", "Pensión alimentaria", "Otro"]
ESTADOS = ["Activo", "En revisión", "Pendiente", "Cerrado", "Finalizado"]
PRIORIDADES = ["Alta", "Media", "Baja", "Urgente"]


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
        self.desplegable(form, "cliente", "Cliente asociado", [], 0, 0, con_placeholder=True)
        self.campo(form, "numero_expediente", "N.º expediente", "Ej. #245", 0, 1)
        self.desplegable(form, "tipo_proceso", "Tipo de proceso", TIPOS_PROCESO, 0, 2)
        self.desplegable(form, "estado", "Estado", ESTADOS, 1, 0)
        self.desplegable(form, "prioridad", "Prioridad", PRIORIDADES, 1, 1)
        self.campo(form, "abogado_responsable", "Abogado responsable", "Lic. responsable", 1, 2, tipo="texto")

    def refrescar(self):
        self._clientes = {c["id_cliente"]: c["nombre_completo"] for c in api.listar("clientes")}
        self.opciones("cliente", list(self._clientes.values()))
        super().refrescar()

    def a_fila(self, r):
        return (r["numero_expediente"], self._clientes.get(r["id_cliente"], "?"),
                r.get("tipo_proceso") or "", r.get("estado") or "",
                r.get("prioridad") or "", r.get("abogado_responsable") or "")

    def validar(self, v):
        if not v["cliente"]:
            return "Debes elegir un cliente. Si no aparece, regístralo primero en Clientes."
        if not v["numero_expediente"]:
            return "El número de expediente es obligatorio."
        return None

    def a_cuerpo(self, v):
        cliente = api.buscar_cliente_por_nombre(v["cliente"])
        if cliente is None:
            raise ValueError(f"No existe un cliente llamado '{v['cliente']}'.")
        return {
            "id_cliente": cliente["id_cliente"],
            "numero_expediente": v["numero_expediente"],
            "tipo_proceso": v["tipo_proceso"] or None,
            "estado": v["estado"] or None,
            "prioridad": v["prioridad"] or None,
            "abogado_responsable": v["abogado_responsable"] or None,
        }

    def llenar_formulario(self, r):
        self.poner("cliente", self._clientes.get(r["id_cliente"], ""))
        self.poner("numero_expediente", r.get("numero_expediente"))
        self.poner("tipo_proceso", r.get("tipo_proceso"))
        self.poner("estado", r.get("estado"))
        self.poner("prioridad", r.get("prioridad"))
        self.poner("abogado_responsable", r.get("abogado_responsable"))
