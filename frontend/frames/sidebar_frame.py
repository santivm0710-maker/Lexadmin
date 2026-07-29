from tkinter import messagebox

import customtkinter as ctk

import icons
from data import MENU_ITEMS
from styles import ACCENT, FONT_FAMILY, SIDEBAR, SIDEBAR_HOVER, SIDEBAR_TEXT

ICONOS = {
    "dashboard": "dashboard", "clientes": "clientes", "casos": "casos", "expedientes": "expedientes",
    "agenda": "agenda", "judicial": "judicial", "reportes": "reportes", "bitacora": "bitacora",
}


class SidebarFrame(ctk.CTkFrame):
    def __init__(self, master, cambiar_pagina):
        super().__init__(master, width=240, fg_color=SIDEBAR, corner_radius=0)
        self.cambiar_pagina = cambiar_pagina
        self.botones = {}
        self.grid_propagate(False)
        self._crear_contenido()

    def _crear_contenido(self):
        marca = ctk.CTkFrame(self, fg_color="transparent")
        marca.pack(fill="x", padx=24, pady=(28, 24))
        insignia = ctk.CTkFrame(marca, width=38, height=38, corner_radius=10, fg_color=ACCENT)
        insignia.pack(side="left")
        insignia.pack_propagate(False)
        ctk.CTkLabel(insignia, text="", image=icons.imagen("logo", 18, "white")).pack(expand=True)
        texto = ctk.CTkFrame(marca, fg_color="transparent")
        texto.pack(side="left", padx=(10, 0))
        ctk.CTkLabel(texto, text="LexAdmin", font=ctk.CTkFont(family=FONT_FAMILY, size=19, weight="bold"),
                     text_color="white").pack(anchor="w")
        ctk.CTkLabel(texto, text="Despacho legal", font=ctk.CTkFont(family=FONT_FAMILY, size=11),
                     text_color=SIDEBAR_TEXT).pack(anchor="w")

        self._iconos_inactivos = {}
        self._iconos_activos = {}
        for clave, etiqueta in MENU_ITEMS:
            nombre_icono = ICONOS.get(clave, "dashboard")
            self._iconos_inactivos[clave] = icons.imagen(nombre_icono, 16, SIDEBAR_TEXT)
            self._iconos_activos[clave] = icons.imagen(nombre_icono, 16, "white")
            boton = ctk.CTkButton(
                self, text=f"  {etiqueta}", image=self._iconos_inactivos[clave], compound="left",
                height=40, anchor="w",
                corner_radius=8, fg_color="transparent", hover_color=SIDEBAR_HOVER,
                text_color=SIDEBAR_TEXT, font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
                command=lambda p=clave: self.cambiar_pagina(p))
            boton.pack(fill="x", padx=14, pady=3)
            self.botones[clave] = boton

        ctk.CTkFrame(self, height=1, fg_color=SIDEBAR_HOVER).pack(fill="x", padx=18, pady=20)
        ctk.CTkLabel(self, text="SESIÓN ACTIVA", text_color="#7C87AC",
                     font=ctk.CTkFont(family=FONT_FAMILY, size=10, weight="bold")).pack(anchor="w", padx=24)
        ctk.CTkLabel(self, text="Abogado principal\nRol: Administrador", justify="left",
                     text_color=SIDEBAR_TEXT, font=ctk.CTkFont(family=FONT_FAMILY, size=12)).pack(anchor="w", padx=24, pady=(4, 20))

        ctk.CTkButton(self, text="Cerrar sesión", image=icons.imagen("salir", 15, SIDEBAR_TEXT), compound="left",
                      height=38, corner_radius=8, fg_color="transparent",
                      hover_color=SIDEBAR_HOVER, border_width=1, border_color=SIDEBAR_HOVER,
                      text_color=SIDEBAR_TEXT, command=self._cerrar_sesion).pack(side="bottom", fill="x", padx=16, pady=24)

    def _cerrar_sesion(self):
        if messagebox.askyesno("Cerrar sesión", "¿Deseas salir de LexAdmin?"):
            self.winfo_toplevel().destroy()

    def marcar_activo(self, pagina):
        for clave, boton in self.botones.items():
            activo = clave == pagina
            boton.configure(
                fg_color=ACCENT if activo else "transparent",
                text_color="white" if activo else SIDEBAR_TEXT,
                image=self._iconos_activos[clave] if activo else self._iconos_inactivos[clave],
            )
