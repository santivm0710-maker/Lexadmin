from tkinter import messagebox

import customtkinter as ctk

from api_client import buscar_id_caso_por_expediente, crear_info_judicial, obtener_judicial
from styles import BG, SUCCESS
from ui_helpers import titulo_seccion, tarjeta, crear_tabla, entrada, actualizar_tabla


class JudicialFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG, corner_radius=0)
        self._crear_contenido()

    def _crear_contenido(self):
        titulo_seccion(self, "Administración de Información Judicial", "Datos visuales de juzgados, jueces, fiscales y entidades relacionadas.")
        form = tarjeta(self)
        form.pack(fill="x", pady=(0, 16))
        for i in range(5):
            form.grid_columnconfigure(i, weight=1)

        self.campo_caso = entrada(form, "Caso", "# expediente")
        self.campo_caso.grid(row=0, column=0, sticky="ew", padx=12, pady=(14, 16))
        self.campo_juzgado = entrada(form, "Juzgado", "Nombre del juzgado")
        self.campo_juzgado.grid(row=0, column=1, sticky="ew", padx=12, pady=(14, 16))
        self.campo_juez = entrada(form, "Juez", "Nombre")
        self.campo_juez.grid(row=0, column=2, sticky="ew", padx=12, pady=(14, 16))
        self.campo_fiscal = entrada(form, "Fiscal", "Nombre")
        self.campo_fiscal.grid(row=0, column=3, sticky="ew", padx=12, pady=(14, 16))
        self.campo_contacto = entrada(form, "Contacto", "correo institucional")
        self.campo_contacto.grid(row=0, column=4, sticky="ew", padx=12, pady=(14, 16))

        ctk.CTkButton(form, text="Guardar datos", fg_color=SUCCESS, hover_color=SUCCESS, command=self._guardar_datos).grid(row=1, column=4, sticky="e", padx=12, pady=(0, 16))

        card = tarjeta(self, "Información judicial registrada")
        card.pack(fill="both", expand=True)
        self.tabla = crear_tabla(card, ("Caso", "Juzgado", "Juez", "Fiscal", "Contacto"), obtener_judicial(), 10)
        self.tabla.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    def _guardar_datos(self):
        caso = self.campo_caso.entry.get().strip()
        juzgado = self.campo_juzgado.entry.get().strip()
        juez = self.campo_juez.entry.get().strip()
        fiscal = self.campo_fiscal.entry.get().strip()
        contacto = self.campo_contacto.entry.get().strip()

        if not caso or not juzgado:
            messagebox.showwarning("Datos incompletos", "Caso y juzgado son obligatorios.")
            return

        id_caso = buscar_id_caso_por_expediente(caso)
        if id_caso is None:
            messagebox.showerror("Caso no encontrado", f"No existe un caso registrado con el expediente '{caso}'.")
            return

        exito, mensaje, _ = crear_info_judicial(id_caso, juzgado, juez, fiscal, contacto)
        if not exito:
            messagebox.showerror("Error al guardar", mensaje)
            return

        for campo in (self.campo_caso, self.campo_juzgado, self.campo_juez, self.campo_fiscal, self.campo_contacto):
            campo.entry.delete(0, "end")
        actualizar_tabla(self.tabla, obtener_judicial())
