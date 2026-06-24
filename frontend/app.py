import customtkinter as ctk

from styles import BG, PRIMARY, PRIMARY_HOVER, TEXT, BORDER, configurar_tema
from frames import (
    SidebarFrame,
    DashboardFrame,
    ClientesFrame,
    CasosFrame,
    ExpedientesFrame,
    AgendaFrame,
    JudicialFrame,
    ReportesFrame,
    BitacoraFrame,
)


class LegalDeskApp(ctk.CTk):
    def __init__(self):
        configurar_tema()
        super().__init__()
        self.title("LexAdmin | Prototipo visual")
        self.geometry("1280x780")
        self.minsize(1120, 700)
        self.configure(fg_color=BG)
        self.pagina_actual = None
        self._crear_layout()
        self._crear_paginas()
        self.mostrar_pagina("dashboard")

    def _crear_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = SidebarFrame(self, self.mostrar_pagina)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.main = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self.main.grid(row=0, column=1, sticky="nsew")
        self.main.grid_rowconfigure(1, weight=1)
        self.main.grid_columnconfigure(0, weight=1)

        self._crear_header()

        self.contenedor = ctk.CTkFrame(self.main, fg_color=BG, corner_radius=0)
        self.contenedor.grid(row=1, column=0, sticky="nsew", padx=24, pady=(8, 24))
        self.contenedor.grid_rowconfigure(0, weight=1)
        self.contenedor.grid_columnconfigure(0, weight=1)

    def _crear_header(self):
        header = ctk.CTkFrame(self.main, fg_color=BG, corner_radius=0)
        header.grid(row=0, column=0, sticky="ew", padx=24, pady=(18, 8))
        header.grid_columnconfigure(0, weight=1)

        self.titulo_header = ctk.CTkLabel(
            header,
            text="Dashboard",
            font=ctk.CTkFont(size=25, weight="bold"),
            text_color=TEXT,
        )
        self.titulo_header.grid(row=0, column=0, sticky="w")

        ctk.CTkEntry(
            header,
            width=330,
            height=40,
            placeholder_text="Buscar cliente, caso o expediente...",
            border_color=BORDER,
            fg_color="white",
        ).grid(row=0, column=1, padx=12)

        ctk.CTkButton(
            header,
            text="+ Nuevo caso",
            height=40,
            width=135,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            corner_radius=10,
            command=lambda: None,
        ).grid(row=0, column=2)

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
        self.titulos = {
            "dashboard": "Dashboard",
            "clientes": "Clientes",
            "casos": "Casos legales",
            "expedientes": "Expedientes",
            "agenda": "Agenda",
            "judicial": "Información judicial",
            "reportes": "Reportes",
            "bitacora": "Bitácora",
        }

    def mostrar_pagina(self, pagina):
        if self.pagina_actual is not None:
            self.pagina_actual.grid_forget()
        self.pagina_actual = self.paginas[pagina]
        self.pagina_actual.grid(row=0, column=0, sticky="nsew")
        self.titulo_header.configure(text=self.titulos[pagina])
        self.sidebar.marcar_activo(pagina)
