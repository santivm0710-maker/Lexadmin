from tkinter import messagebox

import customtkinter as ctk

from api_client import crear_cliente, obtener_clientes
from styles import BG, SUCCESS, INFO
from ui_helpers import titulo_seccion, tarjeta, crear_tabla, entrada, actualizar_tabla


class ClientesFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG, corner_radius=0)
        self._crear_contenido()

    def _crear_contenido(self):
        titulo_seccion(self, "Gestión de Clientes", "Registro visual, consulta e historial asociado a casos legales.")
        self._crear_formulario()
        self._crear_tabla()

    def _crear_formulario(self):
        form = tarjeta(self)
        form.pack(fill="x", pady=(0, 16))
        for i in range(4):
            form.grid_columnconfigure(i, weight=1)

        self.campo_nombre = entrada(form, "Nombre completo", "Ej. Juan Pérez")
        self.campo_nombre.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 16))
        self.campo_cedula = entrada(form, "Identificación", "Ej. 1-1111-1111")
        self.campo_cedula.grid(row=0, column=1, sticky="ew", padx=16, pady=(14, 16))
        self.campo_telefono = entrada(form, "Teléfono", "Ej. 8888-1234")
        self.campo_telefono.grid(row=0, column=2, sticky="ew", padx=16, pady=(14, 16))
        self.campo_correo = entrada(form, "Correo", "cliente@email.com")
        self.campo_correo.grid(row=0, column=3, sticky="ew", padx=16, pady=(14, 16))

        botones = ctk.CTkFrame(form, fg_color="transparent")
        botones.grid(row=1, column=0, columnspan=4, sticky="e", padx=16, pady=(0, 16))
        ctk.CTkButton(botones, text="Buscar cliente", fg_color=INFO, hover_color=INFO, command=lambda: None).pack(side="left", padx=5)
        ctk.CTkButton(botones, text="Guardar cliente", fg_color=SUCCESS, hover_color=SUCCESS, command=self._guardar_cliente).pack(side="left", padx=5)

    def _crear_tabla(self):
        card = tarjeta(self, "Clientes registrados")
        card.pack(fill="both", expand=True)
        self.tabla = crear_tabla(card, ("Cliente", "Identificación", "Teléfono", "Correo", "Caso asociado"), obtener_clientes(), 10)
        self.tabla.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    def _guardar_cliente(self):
        nombre = self.campo_nombre.entry.get().strip()
        cedula = self.campo_cedula.entry.get().strip()
        telefono = self.campo_telefono.entry.get().strip()
        correo = self.campo_correo.entry.get().strip()

        if not nombre or not cedula:
            messagebox.showwarning("Datos incompletos", "Nombre e identificación son obligatorios.")
            return

        exito, mensaje, _ = crear_cliente(nombre, cedula, telefono, correo)
        if not exito:
            messagebox.showerror("Error al guardar", mensaje)
            return

        for campo in (self.campo_nombre, self.campo_cedula, self.campo_telefono, self.campo_correo):
            campo.entry.delete(0, "end")
        actualizar_tabla(self.tabla, obtener_clientes())
