import customtkinter as ctk

import api_client as api
from styles import BG
from ui_helpers import actualizar_tabla, crear_tabla, formatear_fecha, formatear_hora, tarjeta, titulo_seccion


class BitacoraFrame(ctk.CTkFrame):
    """Registro de auditoría, solo de lectura. Se llena automáticamente
    con cada acción realizada en el sistema."""

    columnas = ("Fecha", "Hora", "Actor", "Módulo", "Acción", "Descripción")

    def __init__(self, master):
        super().__init__(master, fg_color=BG, corner_radius=0)
        self._datos = []
        titulo_seccion(self, "Bitácora de Eventos",
                       "Historial automático de auditoría: quién hizo qué y cuándo.")
        card = tarjeta(self, "Eventos registrados")
        card.pack(fill="both", expand=True)
        self.tabla = crear_tabla(card, self.columnas, [], 14)
        self.tabla.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        self.refrescar()

    def _a_fila(self, r):
        return (formatear_fecha(r.get("fecha")), formatear_hora(r.get("hora")),
                r.get("actor") or "", r.get("modulo") or "",
                r.get("accion") or "", r.get("descripcion") or "")

    def refrescar(self):
        self._datos = api.listar("bitacora")
        actualizar_tabla(self.tabla, [self._a_fila(r) for r in self._datos])

    def filtrar(self, texto):
        texto = texto.strip().lower()
        filas = [self._a_fila(r) for r in self._datos
                 if not texto or any(texto in str(c).lower() for c in self._a_fila(r))]
        actualizar_tabla(self.tabla, filas)
