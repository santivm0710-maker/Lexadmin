import customtkinter as ctk

import api_client as api
import icons
from styles import BG, CARD, FONT_FAMILY, MUTED, PRIMARY, ROW_ALT, TEXT
from ui_helpers import crear_tabla, tarjeta, titulo_seccion

ICONOS = {"cliente": "clientes", "caso": "casos", "audiencia": "agenda", "expediente": "expedientes"}


def _icono(titulo):
    for clave, nombre in ICONOS.items():
        if clave in titulo.lower():
            return nombre
    return "dashboard"


class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG, corner_radius=0)
        self.refrescar()

    def refrescar(self):
        for hijo in self.winfo_children():
            hijo.destroy()
        self._construir(api.obtener_dashboard())

    def _construir(self, datos):
        titulo_seccion(self, "Panel principal", "Resumen general del despacho y alertas destacadas.")

        tarjetas = ctk.CTkFrame(self, fg_color="transparent")
        tarjetas.pack(fill="x", pady=(2, 16))
        for i in range(4):
            tarjetas.grid_columnconfigure(i, weight=1)

        for i, (titulo, valor, nota, color) in enumerate(datos.get("stats", [])):
            card = tarjeta(tarjetas)
            card.grid(row=0, column=i, sticky="ew", padx=(0 if i == 0 else 8, 0 if i == 3 else 8))
            ctk.CTkFrame(card, height=3, corner_radius=0, fg_color=color).pack(fill="x")
            cabecera = ctk.CTkFrame(card, fg_color="transparent")
            cabecera.pack(fill="x", padx=18, pady=(16, 2))
            insignia = ctk.CTkFrame(cabecera, width=34, height=34, corner_radius=9, fg_color=ROW_ALT)
            insignia.pack(side="left")
            insignia.pack_propagate(False)
            ctk.CTkLabel(insignia, text="", image=icons.imagen(_icono(titulo), 16, color)).pack(expand=True)
            ctk.CTkLabel(cabecera, text=titulo, font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"),
                         text_color=MUTED).pack(side="left", padx=(10, 0))
            ctk.CTkLabel(card, text=valor, font=ctk.CTkFont(family=FONT_FAMILY, size=30, weight="bold"),
                         text_color=color).pack(anchor="w", padx=18, pady=(6, 0))
            ctk.CTkLabel(card, text=nota, font=ctk.CTkFont(family=FONT_FAMILY, size=12),
                         text_color=MUTED).pack(anchor="w", padx=18, pady=(0, 16))

        cuerpo = ctk.CTkFrame(self, fg_color="transparent")
        cuerpo.pack(fill="both", expand=True)
        cuerpo.grid_columnconfigure(0, weight=2)
        cuerpo.grid_columnconfigure(1, weight=1)
        cuerpo.grid_rowconfigure(0, weight=1)

        izquierda = tarjeta(cuerpo, "Casos que requieren atención")
        izquierda.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        tabla = crear_tabla(izquierda, ("Expediente", "Cliente", "Tipo", "Prioridad", "Estado"),
                            datos.get("casos_atencion", []), 8)
        tabla.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        derecha = tarjeta(cuerpo, "Actividad reciente")
        derecha.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        actividad = datos.get("actividad_reciente", [])
        if not actividad:
            ctk.CTkLabel(derecha, text="Sin actividad todavía.", text_color=MUTED,
                         font=ctk.CTkFont(family=FONT_FAMILY, size=12)).pack(anchor="w", padx=18, pady=10)
        for fecha, actor, modulo, detalle in actividad:
            item = ctk.CTkFrame(derecha, fg_color=ROW_ALT, corner_radius=10)
            item.pack(fill="x", padx=16, pady=6)
            ctk.CTkLabel(item, text=f"{fecha} · {actor}", text_color=PRIMARY,
                         font=ctk.CTkFont(family=FONT_FAMILY, size=11, weight="bold")).pack(anchor="w", padx=12, pady=(8, 0))
            ctk.CTkLabel(item, text=modulo, text_color=TEXT,
                         font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold")).pack(anchor="w", padx=12)
            ctk.CTkLabel(item, text=detalle, text_color=MUTED, wraplength=280, justify="left",
                         font=ctk.CTkFont(family=FONT_FAMILY, size=11)).pack(anchor="w", padx=12, pady=(0, 8))
