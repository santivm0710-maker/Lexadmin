from datetime import datetime
from tkinter import messagebox

import customtkinter as ctk

from api_client import (
    actualizar_evento_agenda,
    buscar_id_caso_por_expediente,
    crear_evento_agenda,
    eliminar_evento_agenda,
    obtener_agenda,
    obtener_agenda_raw,
    obtener_casos_raw,
)
from styles import BG, SUCCESS, INFO, DANGER
from ui_helpers import titulo_seccion, tarjeta, crear_tabla, entrada, actualizar_tabla


class AgendaFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG, corner_radius=0)
        self._editando_id = None
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

        botones = ctk.CTkFrame(form, fg_color="transparent")
        botones.grid(row=2, column=0, columnspan=3, sticky="e", padx=16, pady=(0, 16))
        ctk.CTkButton(botones, text="Eliminar seleccionado", fg_color=DANGER, hover_color=DANGER, command=self._eliminar_seleccionado).pack(side="left", padx=5)
        ctk.CTkButton(botones, text="✎  Editar seleccionado", fg_color=INFO, hover_color=INFO, command=self._cargar_seleccionado).pack(side="left", padx=5)
        self.boton_guardar = ctk.CTkButton(botones, text="＋  Programar", fg_color=SUCCESS, hover_color=SUCCESS, command=self._guardar_evento)
        self.boton_guardar.pack(side="left", padx=5)

        card = tarjeta(self, "Eventos próximos")
        card.pack(fill="both", expand=True)
        self._datos = obtener_agenda_raw()
        ids = [item.get("id_evento") for item in self._datos]
        self.tabla = crear_tabla(card, ("Fecha", "Hora", "Caso", "Actividad", "Lugar", "Estado"), obtener_agenda(), 10, ids)
        self.tabla.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    def _refrescar(self):
        self._datos = obtener_agenda_raw()
        ids = [item.get("id_evento") for item in self._datos]
        actualizar_tabla(self.tabla, obtener_agenda(), ids)

    def _limpiar_formulario(self):
        for campo in (self.campo_fecha, self.campo_hora, self.campo_caso, self.campo_actividad, self.campo_lugar, self.campo_prioridad):
            campo.entry.delete(0, "end")
        self._editando_id = None
        self.boton_guardar.configure(text="＋  Programar")

    def _cargar_seleccionado(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showinfo("Selecciona un evento", "Selecciona una fila de la tabla para editar.")
            return

        item_id = int(seleccion[0])
        item = next((d for d in self._datos if d.get("id_evento") == item_id), None)
        if item is None:
            return

        expedientes_por_id = {c.get("id_caso"): c.get("numero_expediente", "") for c in obtener_casos_raw()}

        try:
            fecha_fmt = datetime.fromisoformat(item.get("fecha", "")).strftime("%d/%m/%Y")
        except ValueError:
            fecha_fmt = item.get("fecha", "")
        hora_valor = str(item.get("hora", ""))[:5]

        self.campo_fecha.entry.delete(0, "end")
        self.campo_fecha.entry.insert(0, fecha_fmt)
        self.campo_hora.entry.delete(0, "end")
        self.campo_hora.entry.insert(0, hora_valor)
        self.campo_caso.entry.delete(0, "end")
        self.campo_caso.entry.insert(0, expedientes_por_id.get(item.get("id_caso"), ""))
        self.campo_actividad.entry.delete(0, "end")
        self.campo_actividad.entry.insert(0, item.get("actividad", ""))
        self.campo_lugar.entry.delete(0, "end")
        self.campo_lugar.entry.insert(0, item.get("lugar", "") or "")
        self.campo_prioridad.entry.delete(0, "end")
        self.campo_prioridad.entry.insert(0, item.get("prioridad", "") or "")

        self._editando_id = item_id
        self.boton_guardar.configure(text="✓  Actualizar evento")

    def _guardar_evento(self):
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

        if self._editando_id is not None:
            exito, mensaje, _ = actualizar_evento_agenda(self._editando_id, id_caso, fecha, hora, actividad, lugar, prioridad)
        else:
            exito, mensaje, _ = crear_evento_agenda(id_caso, fecha, hora, actividad, lugar, prioridad)

        if not exito:
            messagebox.showerror("Error al guardar", mensaje)
            return

        self._limpiar_formulario()
        self._refrescar()

    def _eliminar_seleccionado(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showinfo("Selecciona un evento", "Selecciona una fila de la tabla para eliminar.")
            return

        item_id = int(seleccion[0])
        if not messagebox.askyesno("Confirmar eliminación", "¿Seguro que quieres eliminar este evento?"):
            return

        exito, mensaje, _ = eliminar_evento_agenda(item_id)
        if not exito:
            messagebox.showerror("Error al eliminar", mensaje)
            return

        if self._editando_id == item_id:
            self._limpiar_formulario()
        self._refrescar()
