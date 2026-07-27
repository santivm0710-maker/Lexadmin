import customtkinter as ctk

import api_client as api
from styles import BG, FONT_FAMILY, MUTED
from ui_helpers import crear_tabla, tarjeta, titulo_seccion


class ReportesFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG, corner_radius=0)
        self.refrescar()

    def refrescar(self):
        for hijo in self.winfo_children():
            hijo.destroy()
        self._construir(api.obtener_reportes())

    def _construir(self, datos):
        titulo_seccion(self, "Reportes y Estadísticas",
                       "Indicadores del despacho calculados en tiempo real.")

        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(fill="x", pady=(0, 16))
        for i in range(3):
            grid.grid_columnconfigure(i, weight=1)

        for i, (titulo, valor, color) in enumerate(datos.get("indicadores", [])):
            card = tarjeta(grid)
            card.grid(row=i // 3, column=i % 3, sticky="ew", padx=8, pady=8)
            ctk.CTkLabel(card, text=titulo, text_color=MUTED,
                         font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold")).pack(anchor="w", padx=18, pady=(16, 2))
            ctk.CTkLabel(card, text=valor, text_color=color,
                         font=ctk.CTkFont(family=FONT_FAMILY, size=26, weight="bold")).pack(anchor="w", padx=18, pady=(0, 16))

        card = tarjeta(self, "Resumen por módulo")
        card.pack(fill="both", expand=True)
        tabla = crear_tabla(card, ("Módulo", "Indicador", "Detalle"), datos.get("resumen", []), 8)
        tabla.pack(fill="both", expand=True, padx=18, pady=(0, 18))
