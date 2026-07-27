from datetime import datetime

import api_client as api
from crud_frame import CrudFrame
from ui_helpers import formatear_fecha, formatear_hora


class AgendaFrame(CrudFrame):
    recurso = "agenda"
    pk = "id_agenda"
    titulo = "Agenda y Audiencias"
    subtitulo = "Programación de audiencias, reuniones y vencimientos por caso."
    titulo_tabla = "Eventos programados"
    columnas = ("Fecha", "Hora", "Caso", "Actividad", "Lugar", "Prioridad")
    columnas_form = 3
    texto_crear = "Programar"
    texto_actualizar = "Actualizar evento"

    def definir_campos(self, form):
        self.campo(form, "fecha", "Fecha", "dd/mm/aaaa", 0, 0, tipo="fecha")
        self.campo(form, "hora", "Hora", "hh:mm", 0, 1, tipo="hora")
        self.campo(form, "caso", "Caso (expediente)", "Ej. #245", 0, 2)
        self.campo(form, "actividad", "Actividad", "Audiencia / Reunión", 1, 0, tipo="texto")
        self.campo(form, "lugar", "Lugar", "Juzgado / Sala", 1, 1)
        self.campo(form, "prioridad", "Prioridad", "Alta / Media", 1, 2, tipo="texto")

    def refrescar(self):
        self._casos = {c["id_caso"]: c for c in api.listar("casos")}
        super().refrescar()

    def a_fila(self, r):
        caso = self._casos.get(r["id_caso"], {})
        return (formatear_fecha(r.get("fecha")), formatear_hora(r.get("hora")),
                caso.get("numero_expediente", "?"), r.get("actividad") or "",
                r.get("lugar") or "", r.get("prioridad") or "")

    def validar(self, v):
        if not v["fecha"] or not v["hora"] or not v["caso"] or not v["actividad"]:
            return "Fecha, hora, caso y actividad son obligatorios."
        return None

    def a_cuerpo(self, v):
        try:
            fecha = datetime.strptime(v["fecha"], "%d/%m/%Y").date().isoformat()
        except ValueError:
            raise ValueError("La fecha debe tener el formato dd/mm/aaaa.")
        try:
            hora = datetime.strptime(v["hora"], "%H:%M").strftime("%H:%M:%S")
        except ValueError:
            raise ValueError("La hora debe tener el formato hh:mm (24 horas).")
        caso = api.buscar_caso_por_expediente(v["caso"])
        if caso is None:
            raise ValueError(f"No existe un caso con expediente '{v['caso']}'.")
        return {
            "id_caso": caso["id_caso"],
            "fecha": fecha,
            "hora": hora,
            "actividad": v["actividad"],
            "lugar": v["lugar"] or None,
            "prioridad": v["prioridad"] or None,
        }

    def llenar_formulario(self, r):
        caso = self._casos.get(r["id_caso"], {})
        self.poner("fecha", formatear_fecha(r.get("fecha")))
        self.poner("hora", formatear_hora(r.get("hora")))
        self.poner("caso", caso.get("numero_expediente"))
        self.poner("actividad", r.get("actividad"))
        self.poner("lugar", r.get("lugar"))
        self.poner("prioridad", r.get("prioridad"))
