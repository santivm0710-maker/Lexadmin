from crud_frame import CrudFrame
from ui_helpers import formatear_fecha, validar_email


class ClientesFrame(CrudFrame):
    recurso = "clientes"
    pk = "id_cliente"
    titulo = "Gestión de Clientes"
    subtitulo = "Registro, consulta e historial de los clientes del despacho."
    titulo_tabla = "Clientes registrados"
    columnas = ("Cliente", "Identificación", "Teléfono", "Correo", "Registrado")
    columnas_form = 4
    texto_crear = "Guardar cliente"
    texto_actualizar = "Actualizar cliente"

    def definir_campos(self, form):
        self.campo(form, "nombre_completo", "Nombre completo", "Ej. Juan Pérez", 0, 0, tipo="texto")
        self.campo(form, "identificacion", "Identificación", "Ej. 1-1111-1111", 0, 1, tipo="identificacion")
        self.campo(form, "telefono", "Teléfono", "Ej. 8888-1234", 0, 2, tipo="telefono")
        self.campo(form, "correo", "Correo", "cliente@correo.com", 0, 3)

    def a_fila(self, r):
        return (r["nombre_completo"], r["identificacion"], r.get("telefono") or "",
                r.get("correo") or "", formatear_fecha(r.get("fecha_registro")))

    def validar(self, v):
        if not v["nombre_completo"] or not v["identificacion"]:
            return "El nombre y la identificación son obligatorios."
        if v["correo"] and not validar_email(v["correo"]):
            return "El correo no tiene un formato válido."
        return None

    def a_cuerpo(self, v):
        return {
            "nombre_completo": v["nombre_completo"],
            "identificacion": v["identificacion"],
            "telefono": v["telefono"] or None,
            "correo": v["correo"] or None,
        }

    def llenar_formulario(self, r):
        self.poner("nombre_completo", r.get("nombre_completo"))
        self.poner("identificacion", r.get("identificacion"))
        self.poner("telefono", r.get("telefono"))
        self.poner("correo", r.get("correo"))
