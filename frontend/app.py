import customtkinter as ctk

from styles import ACCENT, ACCENT_HOVER, BG, BORDER, CARD, FONT_FAMILY, TEXT, configurar_tema
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
        self.contenedor.grid(row=1, column=0, sticky="nsew", padx=28, pady=(8, 24))
        self.contenedor.grid_rowconfigure(0, weight=1)
        self.contenedor.grid_columnconfigure(0, weight=1)

    def _crear_header(self):
        header = ctk.CTkFrame(self.main, fg_color=BG, corner_radius=0)
        header.grid(row=0, column=0, sticky="ew", padx=28, pady=(22, 10))
        header.grid_columnconfigure(0, weight=1)

        self.titulo_header = ctk.CTkLabel(
            header,
            text="Dashboard",
            font=ctk.CTkFont(family=FONT_FAMILY, size=24, weight="bold"),
            text_color=TEXT,
        )
        self.titulo_header.grid(row=0, column=0, sticky="w")

        buscador = ctk.CTkFrame(header, height=38, corner_radius=10, fg_color=CARD, border_width=1, border_color=BORDER)
        buscador.grid(row=0, column=1, padx=12)
        buscador.grid_propagate(False)
        buscador.configure(width=320)
        ctk.CTkLabel(buscador, text="🔍", font=ctk.CTkFont(size=13), text_color=TEXT).pack(side="left", padx=(12, 4))
        ctk.CTkEntry(
            buscador,
            fg_color="transparent",
            border_width=0,
            placeholder_text="Buscar cliente, caso o expediente...",
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
        ).pack(side="left", fill="both", expand=True, padx=(0, 12))

        ctk.CTkButton(
            header,
            text="+ Nuevo caso",
            height=38,
            width=130,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            corner_radius=8,
            font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"),
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
