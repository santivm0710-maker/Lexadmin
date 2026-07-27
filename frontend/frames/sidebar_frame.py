import customtkinter as ctk

from data import MENU_ITEMS
from styles import ACCENT, SIDEBAR, SIDEBAR_HOVER, FONT_FAMILY

ICONOS = {
    "dashboard": "⬚",
    "clientes": "☺",
    "casos": "⚖",
    "expedientes": "🗀",
    "agenda": "🗓",
    "judicial": "🏛",
    "reportes": "📊",
    "bitacora": "🕓",
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

        badge = ctk.CTkFrame(marca, width=36, height=36, corner_radius=10, fg_color=ACCENT)
        badge.pack(side="left")
        badge.pack_propagate(False)
        ctk.CTkLabel(badge, text="⚖", font=ctk.CTkFont(size=17), text_color="white").pack(expand=True)

        texto = ctk.CTkFrame(marca, fg_color="transparent")
        texto.pack(side="left", padx=(10, 0))
        ctk.CTkLabel(
            texto,
            text="LexAdmin",
            font=ctk.CTkFont(family=FONT_FAMILY, size=19, weight="bold"),
            text_color="white",
        ).pack(anchor="w")
        ctk.CTkLabel(
            texto,
            text="Despacho legal",
            font=ctk.CTkFont(family=FONT_FAMILY, size=11),
            text_color="#9CA6C4",
        ).pack(anchor="w")

        for clave, texto in MENU_ITEMS:
            icono = ICONOS.get(clave, "•")
            boton = ctk.CTkButton(
                self,
                text=f"  {icono}   {texto}",
                height=40,
                anchor="w",
                corner_radius=8,
                fg_color="transparent",
                hover_color=SIDEBAR_HOVER,
                text_color="#D1D5E3",
                font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
                command=lambda pagina=clave: self.cambiar_pagina(pagina),
            )
            boton.pack(fill="x", padx=14, pady=3)
            self.botones[clave] = boton

        ctk.CTkFrame(self, height=1, fg_color=SIDEBAR_HOVER).pack(fill="x", padx=18, pady=22)
        ctk.CTkLabel(self, text="Sesión activa", text_color="#7C87AC", font=ctk.CTkFont(family=FONT_FAMILY, size=11, weight="bold")).pack(anchor="w", padx=24)
        ctk.CTkLabel(self, text="Abogado principal\nRol: Administrador", justify="left", text_color="#D1D5E3", font=ctk.CTkFont(family=FONT_FAMILY, size=12)).pack(anchor="w", padx=24, pady=(4, 20))

        ctk.CTkButton(
            self,
            text="Cerrar sesión",
            height=38,
            fg_color="transparent",
            hover_color=SIDEBAR_HOVER,
            border_width=1,
            border_color=SIDEBAR_HOVER,
            text_color="#D1D5E3",
            corner_radius=8,
            command=lambda: None,
        ).pack(side="bottom", fill="x", padx=16, pady=24)

    def marcar_activo(self, pagina):
        for clave, boton in self.botones.items():
            activo = clave == pagina
            boton.configure(
                fg_color=ACCENT if activo else "transparent",
                text_color="white" if activo else "#D1D5E3",
            )
