import customtkinter as ctk

from api_client import obtener_judicial
from styles import BG, SUCCESS
from ui_helpers import titulo_seccion, tarjeta, crear_tabla, entrada


class JudicialFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG, corner_radius=0)
        self._crear_contenido()

    def _crear_contenido(self):
        titulo_seccion(self, "Administración de Información Judicial", "Datos visuales de juzgados, jueces, fiscales y entidades relacionadas.")
        form = tarjeta(self)
        form.pack(fill="x", pady=(0, 16))
        campos = [("Caso", "# expediente"), ("Juzgado", "Nombre del juzgado"), ("Juez", "Nombre"), ("Fiscal", "Nombre"), ("Contacto", "correo institucional")]
        for i in range(5):
            form.grid_columnconfigure(i, weight=1)
        for i, (label, ph) in enumerate(campos):
            entrada(form, label, ph).grid(row=0, column=i, sticky="ew", padx=12, pady=(14, 16))
        ctk.CTkButton(form, text="Guardar datos", fg_color=SUCCESS, hover_color=SUCCESS, command=lambda: None).grid(row=1, column=4, sticky="e", padx=12, pady=(0, 16))

        card = tarjeta(self, "Información judicial registrada")
        card.pack(fill="both", expand=True)
        crear_tabla(card, ("Caso", "Juzgado", "Juez", "Fiscal", "Contacto"), obtener_judicial(), 10).pack(fill="both", expand=True, padx=18, pady=(0, 18))
