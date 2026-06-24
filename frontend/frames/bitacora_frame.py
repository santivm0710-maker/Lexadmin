from api_client import obtener_bitacora
from styles import BG
from ui_helpers import titulo_seccion, tarjeta, crear_tabla, entrada
import customtkinter as ctk


class BitacoraFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG, corner_radius=0)
        self._crear_contenido()

    def _crear_contenido(self):
        titulo_seccion(self, "Bitácora de Eventos", "Registro visual de auditoría: usuario, fecha, hora, módulo y acción realizada.")
        filtros = tarjeta(self)
        filtros.pack(fill="x", pady=(0, 16))
        campos = [("Fecha", "dd/mm/aaaa"), ("Actor", "Abogado / Sistema"), ("Módulo", "Gestión, OCR, Logs"), ("Acción", "Buscar acción")]
        for i in range(4):
            filtros.grid_columnconfigure(i, weight=1)
        for i, (label, ph) in enumerate(campos):
            entrada(filtros, label, ph).grid(row=0, column=i, sticky="ew", padx=16, pady=(14, 16))

        card = tarjeta(self, "Eventos registrados")
        card.pack(fill="both", expand=True)
        crear_tabla(card, ("Fecha", "Actor", "Módulo", "Acción", "Descripción"), obtener_bitacora(), 12).pack(fill="both", expand=True, padx=18, pady=(0, 18))
