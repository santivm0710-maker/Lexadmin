import customtkinter as ctk

from api_client import obtener_expedientes
from styles import BG, SUCCESS
from ui_helpers import titulo_seccion, tarjeta, crear_tabla, entrada


class ExpedientesFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG, corner_radius=0)
        self._crear_contenido()

    def _crear_contenido(self):
        titulo_seccion(self, "Digitalización y Expedientes", "Carga visual de PDF, OCR pendiente y organización Cliente → Caso → Documento.")
        form = tarjeta(self)
        form.pack(fill="x", pady=(0, 16))
        for i in range(4):
            form.grid_columnconfigure(i, weight=1)
        campos = [("Cliente", "Cliente registrado"), ("Caso", "# expediente"), ("Documento PDF", "archivo.pdf"), ("Tipo documento", "Expediente / Prueba")]
        for i, (label, ph) in enumerate(campos):
            entrada(form, label, ph).grid(row=0, column=i, sticky="ew", padx=16, pady=(14, 16))
        ctk.CTkButton(form, text="Subir PDF", fg_color=SUCCESS, hover_color=SUCCESS, command=lambda: None).grid(row=1, column=3, sticky="e", padx=16, pady=(0, 16))

        card = tarjeta(self, "Documentos digitalizados")
        card.pack(fill="both", expand=True)
        crear_tabla(card, ("Cliente", "Caso", "Archivo", "Tipo", "OCR", "Estructura"), obtener_expedientes(), 10).pack(fill="both", expand=True, padx=18, pady=(0, 18))
