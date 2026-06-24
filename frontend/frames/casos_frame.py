import customtkinter as ctk

from api_client import obtener_casos
from styles import BG, SUCCESS
from ui_helpers import titulo_seccion, tarjeta, crear_tabla, entrada


class CasosFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG, corner_radius=0)
        self._crear_contenido()

    def _crear_contenido(self):
        titulo_seccion(self, "Gestión de Casos Legales", "Creación, actualización y seguimiento visual de expedientes jurídicos.")
        form = tarjeta(self)
        form.pack(fill="x", pady=(0, 16))
        campos = [
            ("Cliente asociado", "Seleccione cliente registrado"),
            ("Número expediente", "Debe ser único"),
            ("Tipo de proceso", "Civil, laboral, familia..."),
            ("Estado", "Activo / En revisión"),
            ("Prioridad", "Alta / Urgente"),
            ("Abogado responsable", "Lic. responsable"),
        ]
        for i in range(3):
            form.grid_columnconfigure(i, weight=1)
        for i, (label, ph) in enumerate(campos):
            entrada(form, label, ph).grid(row=i // 3, column=i % 3, sticky="ew", padx=16, pady=(14, 12))
        ctk.CTkButton(form, text="Crear caso", fg_color=SUCCESS, hover_color=SUCCESS, command=lambda: None).grid(row=2, column=2, sticky="e", padx=16, pady=(0, 16))

        card = tarjeta(self, "Casos registrados")
        card.pack(fill="both", expand=True)
        crear_tabla(card, ("Expediente", "Cliente", "Tipo", "Estado", "Prioridad", "Responsable"), obtener_casos(), 10).pack(fill="both", expand=True, padx=18, pady=(0, 18))
