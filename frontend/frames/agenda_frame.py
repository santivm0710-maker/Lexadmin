from datetime import datetime
from tkinter import messagebox

import customtkinter as ctk

from api_client import buscar_id_caso_por_expediente, crear_evento_agenda, obtener_agenda
from styles import BG, SUCCESS
from ui_helpers import titulo_seccion, tarjeta, crear_tabla, entrada, actualizar_tabla


class AgendaFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG, corner_radius=0)
        self._crear_contenido()

    def _crear_contenido(self):
        titulo_seccion(self, "Agenda y Audiencias", "Programación visual de audiencias, reuniones, vencimientos y recordatorios.")
        form = tarjeta(self)
        form.pack(fill="x", pady=(0, 16))
        for i in range(3):
            form.grid_columnconfigure(i, weight=1)

        self.campo_fecha = entrada(form, "Fecha", "dd/mm/aaaa")
        self.campo_fecha.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 12))
        self.campo_hora = entrada(form, "Hora", "hh:mm")
        self.campo_hora.grid(row=0, column=1, sticky="ew", padx=16, pady=(14, 12))
        self.campo_caso = entrada(form, "Caso", "# expediente")
        self.campo_caso.grid(row=0, column=2, sticky="ew", padx=16, pady=(14, 12))
        self.campo_actividad = entrada(form, "Actividad", "Audiencia / Reunión")
        self.campo_actividad.grid(row=1, column=0, sticky="ew", padx=16, pady=(14, 12))
        self.campo_lugar = entrada(form, "Lugar", "Juzgado / Sala")
        self.campo_lugar.grid(row=1, column=1, sticky="ew", padx=16, pady=(14, 12))
        self.campo_prioridad = entrada(form, "Prioridad", "Alta / Urgente")
        self.campo_prioridad.grid(row=1, column=2, sticky="ew", padx=16, pady=(14, 12))

        ctk.CTkButton(form, text="Programar", fg_color=SUCCESS, hover_color=SUCCESS, command=self._programar_evento).grid(row=2, column=2, sticky="e", padx=16, pady=(0, 16))

        card = tarjeta(self, "Eventos próximos")
        card.pack(fill="both", expand=True)
        self.tabla = crear_tabla(card, ("Fecha", "Hora", "Caso", "Actividad", "Lugar", "Estado"), obtener_agenda(), 10)
        self.tabla.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    def _programar_evento(self):
        fecha_txt = self.campo_fecha.entry.get().strip()
        hora_txt = self.campo_hora.entry.get().strip()
        caso = self.campo_caso.entry.get().strip()
        actividad = self.campo_actividad.entry.get().strip()
        lugar = self.campo_lugar.entry.get().strip()
        prioridad = self.campo_prioridad.entry.get().strip()

        if not fecha_txt or not hora_txt or not caso or not actividad:
            messagebox.showwarning("Datos incompletos", "Fecha, hora, caso y actividad son obligatorios.")
            return

        try:
            fecha = datetime.strptime(fecha_txt, "%d/%m/%Y").date().isoformat()
        except ValueError:
            messagebox.showerror("Fecha inválida", "Usa el formato dd/mm/aaaa.")
            return

        try:
            hora = datetime.strptime(hora_txt, "%H:%M").time().isoformat()
        except ValueError:
            messagebox.showerror("Hora inválida", "Usa el formato hh:mm.")
            return

        id_caso = buscar_id_caso_por_expediente(caso)
        if id_caso is None:
            messagebox.showerror("Caso no encontrado", f"No existe un caso registrado con el expediente '{caso}'.")
            return

        exito, mensaje, _ = crear_evento_agenda(id_caso, fecha, hora, actividad, lugar, prioridad)
        if not exito:
            messagebox.showerror("Error al guardar", mensaje)
            return

        for campo in (self.campo_fecha, self.campo_hora, self.campo_caso, self.campo_actividad, self.campo_lugar, self.campo_prioridad):
            campo.entry.delete(0, "end")
        actualizar_tabla(self.tabla, obtener_agenda())
