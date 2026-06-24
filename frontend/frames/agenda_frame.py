import customtkinter as ctk

from api_client import obtener_agenda
from styles import BG, SUCCESS
from ui_helpers import titulo_seccion, tarjeta, crear_tabla, entrada


class AgendaFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG, corner_radius=0)
        self._crear_contenido()

    def _crear_contenido(self):
        titulo_seccion(self, "Agenda y Audiencias", "Programación visual de audiencias, reuniones, vencimientos y recordatorios.")
        form = tarjeta(self)
        form.pack(fill="x", pady=(0, 16))
        campos = [("Fecha", "dd/mm/aaaa"), ("Hora", "hh:mm"), ("Caso", "# expediente"), ("Actividad", "Audiencia / Reunión"), ("Lugar", "Juzgado / Sala"), ("Prioridad", "Alta / Urgente")]
        for i in range(3):
            form.grid_columnconfigure(i, weight=1)
        for i, (label, ph) in enumerate(campos):
            entrada(form, label, ph).grid(row=i // 3, column=i % 3, sticky="ew", padx=16, pady=(14, 12))
        ctk.CTkButton(form, text="Programar", fg_color=SUCCESS, hover_color=SUCCESS, command=lambda: None).grid(row=2, column=2, sticky="e", padx=16, pady=(0, 16))

        card = tarjeta(self, "Eventos próximos")
        card.pack(fill="both", expand=True)
        crear_tabla(card, ("Fecha", "Hora", "Caso", "Actividad", "Lugar", "Estado"), obtener_agenda(), 10).pack(fill="both", expand=True, padx=18, pady=(0, 18))
