import customtkinter as ctk

from api_client import obtener_reportes, obtener_indicadores_reportes
from styles import BG, PRIMARY, SUCCESS, WARNING, DANGER, INFO, MUTED
from ui_helpers import titulo_seccion, tarjeta, crear_tabla


class ReportesFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG, corner_radius=0)
        self._crear_contenido()

    def _crear_contenido(self):
        titulo_seccion(self, "Reportes y Estadísticas", "Indicadores visuales para apoyar la toma de decisiones del despacho.")
        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(fill="x", pady=(0, 16))
        for i in range(3):
            grid.grid_columnconfigure(i, weight=1)
        indicadores = obtener_indicadores_reportes() or [("Casos activos", "46", INFO), ("Casos finalizados", "82", SUCCESS), ("Urgentes", "8", DANGER), ("Audiencias", "14", WARNING), ("PDF OCR", "289", SUCCESS), ("Eventos bitácora", "1,240", PRIMARY)]
        for i, (titulo, valor, color) in enumerate(indicadores):
            card = tarjeta(grid)
            card.grid(row=i // 3, column=i % 3, sticky="ew", padx=8, pady=8)
            ctk.CTkLabel(card, text=titulo, text_color=MUTED, font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=18, pady=(16, 2))
            ctk.CTkLabel(card, text=valor, text_color=color, font=ctk.CTkFont(size=27, weight="bold")).pack(anchor="w", padx=18, pady=(0, 16))

        card = tarjeta(self, "Resumen por módulo")
        card.pack(fill="both", expand=True)
        crear_tabla(card, ("Módulo", "Indicador", "Detalle"), obtener_reportes(), 8).pack(fill="both", expand=True, padx=18, pady=(0, 18))
