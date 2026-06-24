import customtkinter as ctk

from api_client import obtener_dashboard_stats, obtener_casos_atencion, obtener_actividad_reciente
from styles import BG, TEXT, MUTED, PRIMARY
from ui_helpers import titulo_seccion, tarjeta, crear_tabla


class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG, corner_radius=0)
        self._crear_contenido()

    def _crear_contenido(self):
        titulo_seccion(self, "Dashboard", "Resumen general del despacho legal y alertas principales.")

        stats = ctk.CTkFrame(self, fg_color="transparent")
        stats.pack(fill="x", pady=(2, 16))
        for i in range(4):
            stats.grid_columnconfigure(i, weight=1)

        for i, (titulo, valor, nota, color) in enumerate(obtener_dashboard_stats()):
            card = tarjeta(stats)
            card.grid(row=0, column=i, sticky="ew", padx=(0 if i == 0 else 8, 0 if i == 3 else 8))
            ctk.CTkLabel(card, text=titulo, font=ctk.CTkFont(size=13, weight="bold"), text_color=MUTED).pack(anchor="w", padx=18, pady=(16, 2))
            ctk.CTkLabel(card, text=valor, font=ctk.CTkFont(size=30, weight="bold"), text_color=color).pack(anchor="w", padx=18)
            ctk.CTkLabel(card, text=nota, font=ctk.CTkFont(size=12), text_color=MUTED).pack(anchor="w", padx=18, pady=(0, 16))

        contenido = ctk.CTkFrame(self, fg_color="transparent")
        contenido.pack(fill="both", expand=True)
        contenido.grid_columnconfigure(0, weight=2)
        contenido.grid_columnconfigure(1, weight=1)
        contenido.grid_rowconfigure(0, weight=1)

        card_casos = tarjeta(contenido, "Casos que requieren atención")
        card_casos.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        tabla = crear_tabla(card_casos, ("Expediente", "Cliente", "Tipo", "Prioridad", "Estado"), obtener_casos_atencion(), 8)
        tabla.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        card_actividad = tarjeta(contenido, "Actividad reciente")
        card_actividad.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        for fecha, actor, modulo, detalle in obtener_actividad_reciente():
            item = ctk.CTkFrame(card_actividad, fg_color="#F8FAFC", corner_radius=12)
            item.pack(fill="x", padx=18, pady=6)
            ctk.CTkLabel(item, text=f"{fecha} · {actor}", text_color=PRIMARY, font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=12, pady=(8, 0))
            ctk.CTkLabel(item, text=modulo, text_color=TEXT, font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=12)
            ctk.CTkLabel(item, text=detalle, text_color=MUTED, wraplength=290, justify="left").pack(anchor="w", padx=12, pady=(0, 8))
