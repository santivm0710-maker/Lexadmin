import customtkinter as ctk

import icons
from styles import ACCENT, ACCENT_HOVER, BG, BORDER, CARD, FONT_FAMILY, MUTED, TEXT, configurar_tema
from frames import (
    SidebarFrame, DashboardFrame, ClientesFrame, CasosFrame, ExpedientesFrame,
    AgendaFrame, JudicialFrame, ReportesFrame, BitacoraFrame,
)

TITULOS = {
    "dashboard": "Panel principal", "clientes": "Clientes", "casos": "Casos legales",
    "expedientes": "Expedientes", "agenda": "Agenda", "judicial": "Información judicial",
    "reportes": "Reportes", "bitacora": "Bitácora",
}


class LegalDeskApp(ctk.CTk):
    def __init__(self, usuario=None):
        configurar_tema()
        super().__init__()
        icons.imagen.cache_clear()  # los íconos cacheados pertenecían a una raíz de Tk ya destruida
        self.title("LexAdmin | Gestión de despacho legal")
        self.geometry("1300x800")
        self.minsize(1120, 700)
        self.configure(fg_color=BG)
        self.usuario = usuario
        self.solicito_cerrar_sesion = False
        self.pagina_actual = None
        self._crear_layout()
        self._crear_paginas()
        self.mostrar_pagina("dashboard")

    def _crear_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = SidebarFrame(self, self.mostrar_pagina, self.usuario, self._cerrar_sesion)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.main = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self.main.grid(row=0, column=1, sticky="nsew")
        self.main.grid_rowconfigure(1, weight=1)
        self.main.grid_columnconfigure(0, weight=1)

        self._crear_header()

        self.contenedor = ctk.CTkFrame(self.main, fg_color=BG, corner_radius=0)
        self.contenedor.grid(row=1, column=0, sticky="nsew", padx=28, pady=(8, 24))
        self.contenedor.grid_rowconfigure(0, weight=1)
        self.contenedor.grid_columnconfigure(0, weight=1)

    def _crear_header(self):
        header = ctk.CTkFrame(self.main, fg_color=BG, corner_radius=0)
        header.grid(row=0, column=0, sticky="ew", padx=28, pady=(22, 10))
        header.grid_columnconfigure(0, weight=1)

        self.titulo_header = ctk.CTkLabel(
            header, text="Panel principal",
            font=ctk.CTkFont(family=FONT_FAMILY, size=24, weight="bold"), text_color=TEXT)
        self.titulo_header.grid(row=0, column=0, sticky="w")

        buscador = ctk.CTkFrame(header, width=300, height=38, corner_radius=10,
                                fg_color=CARD, border_width=1, border_color=BORDER)
        buscador.grid(row=0, column=1, padx=12)
        buscador.grid_propagate(False)
        ctk.CTkLabel(buscador, text="", image=icons.imagen("buscar", 14, MUTED)).pack(side="left", padx=(12, 4))
        self.busqueda = ctk.CTkEntry(buscador, fg_color="transparent", border_width=0,
                                     placeholder_text="Buscar en esta sección...",
                                     font=ctk.CTkFont(family=FONT_FAMILY, size=12))
        self.busqueda.pack(side="left", fill="both", expand=True, padx=(0, 12))
        self.busqueda.bind("<KeyRelease>", self._al_buscar)

        ctk.CTkButton(header, text="Nuevo caso", image=icons.imagen("agregar", 15, "white"), compound="left",
                      height=38, width=150, corner_radius=8,
                      fg_color=ACCENT, hover_color=ACCENT_HOVER,
                      font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"),
                      command=lambda: self.mostrar_pagina("casos")).grid(row=0, column=2)

    def _crear_paginas(self):
        self.paginas = {
            "dashboard": DashboardFrame(self.contenedor),
            "clientes": ClientesFrame(self.contenedor),
            "casos": CasosFrame(self.contenedor),
            "expedientes": ExpedientesFrame(self.contenedor),
            "agenda": AgendaFrame(self.contenedor),
            "judicial": JudicialFrame(self.contenedor),
            "reportes": ReportesFrame(self.contenedor),
            "bitacora": BitacoraFrame(self.contenedor),
        }

    def mostrar_pagina(self, pagina):
        if self.pagina_actual is not None:
            self.pagina_actual.grid_forget()
        self.pagina_actual = self.paginas[pagina]
        self.pagina_actual.grid(row=0, column=0, sticky="nsew")
        self.titulo_header.configure(text=TITULOS[pagina])
        self.sidebar.marcar_activo(pagina)

        # Al entrar a una sección, se recargan sus datos desde el backend.
        if hasattr(self.pagina_actual, "refrescar"):
            self.pagina_actual.refrescar()
        self.busqueda.delete(0, "end")

    def _al_buscar(self, _evento=None):
        texto = self.busqueda.get()
        if hasattr(self.pagina_actual, "filtrar"):
            self.pagina_actual.filtrar(texto)

    def _cerrar_sesion(self):
        self.solicito_cerrar_sesion = True
        self.destroy()


if __name__ == "__main__":
    LegalDeskApp().mainloop()
