import customtkinter as ctk

from data import MENU_ITEMS
from styles import PRIMARY, PRIMARY_HOVER


class SidebarFrame(ctk.CTkFrame):
    def __init__(self, master, cambiar_pagina):
        super().__init__(master, width=240, fg_color=PRIMARY, corner_radius=0)
        self.cambiar_pagina = cambiar_pagina
        self.botones = {}
        self.grid_propagate(False)
        self._crear_contenido()

    def _crear_contenido(self):
        ctk.CTkLabel(
            self,
            text="LexAdmin",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="white",
        ).pack(anchor="w", padx=24, pady=(28, 2))

        ctk.CTkLabel(
            self,
            text="Gestión de despacho legal",
            font=ctk.CTkFont(size=13),
            text_color="#BFDBFE",
        ).pack(anchor="w", padx=24, pady=(0, 24))

        for clave, texto in MENU_ITEMS:
            boton = ctk.CTkButton(
                self,
                text=texto,
                height=42,
                anchor="w",
                corner_radius=10,
                fg_color="transparent",
                hover_color=PRIMARY_HOVER,
                text_color="white",
                font=ctk.CTkFont(size=14, weight="bold"),
                command=lambda pagina=clave: self.cambiar_pagina(pagina),
            )
            boton.pack(fill="x", padx=16, pady=4)
            self.botones[clave] = boton

        ctk.CTkFrame(self, height=1, fg_color="#3B82F6").pack(fill="x", padx=18, pady=20)
        ctk.CTkLabel(self, text="Sesión activa", text_color="#BFDBFE", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=24)
        ctk.CTkLabel(self, text="Abogado principal\nRol: Administrador", justify="left", text_color="white").pack(anchor="w", padx=24, pady=(4, 20))

        ctk.CTkButton(
            self,
            text="Cerrar sesión",
            height=38,
            fg_color="#0F172A",
            hover_color="#111827",
            corner_radius=10,
            command=lambda: None,
        ).pack(side="bottom", fill="x", padx=16, pady=24)

    def marcar_activo(self, pagina):
        for clave, boton in self.botones.items():
            boton.configure(fg_color="#3B82F6" if clave == pagina else "transparent")
