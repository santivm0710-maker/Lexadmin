from tkinter import messagebox

import customtkinter as ctk

from api_client import (
    actualizar_cliente,
    crear_cliente,
    eliminar_cliente,
    obtener_clientes,
    obtener_clientes_raw,
)
from styles import BG, SUCCESS, INFO, DANGER
from ui_helpers import titulo_seccion, tarjeta, crear_tabla, entrada, actualizar_tabla


class ClientesFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG, corner_radius=0)
        self._editando_id = None
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
        ctk.CTkButton(botones, text="Eliminar seleccionado", fg_color=DANGER, hover_color=DANGER, command=self._eliminar_seleccionado).pack(side="left", padx=5)
        ctk.CTkButton(botones, text="✎  Editar seleccionado", fg_color=INFO, hover_color=INFO, command=self._cargar_seleccionado).pack(side="left", padx=5)
        self.boton_guardar = ctk.CTkButton(botones, text="＋  Guardar cliente", fg_color=SUCCESS, hover_color=SUCCESS, command=self._guardar_cliente)
        self.boton_guardar.pack(side="left", padx=5)

    def _crear_tabla(self):
        card = tarjeta(self, "Clientes registrados")
        card.pack(fill="both", expand=True)
        self._datos = obtener_clientes_raw()
        ids = [item.get("id_cliente") for item in self._datos]
        self.tabla = crear_tabla(card, ("Cliente", "Identificación", "Teléfono", "Correo", "Caso asociado"), obtener_clientes(), 10, ids)
        self.tabla.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    def _refrescar(self):
        self._datos = obtener_clientes_raw()
        ids = [item.get("id_cliente") for item in self._datos]
        actualizar_tabla(self.tabla, obtener_clientes(), ids)

    def _limpiar_formulario(self):
        for campo in (self.campo_nombre, self.campo_cedula, self.campo_telefono, self.campo_correo):
            campo.entry.delete(0, "end")
        self._editando_id = None
        self.boton_guardar.configure(text="＋  Guardar cliente")

    def _cargar_seleccionado(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showinfo("Selecciona un cliente", "Selecciona una fila de la tabla para editar.")
            return

        item_id = int(seleccion[0])
        item = next((d for d in self._datos if d.get("id_cliente") == item_id), None)
        if item is None:
            return

        self.campo_nombre.entry.delete(0, "end")
        self.campo_nombre.entry.insert(0, item.get("nombre", ""))
        self.campo_cedula.entry.delete(0, "end")
        self.campo_cedula.entry.insert(0, item.get("cedula", ""))
        self.campo_telefono.entry.delete(0, "end")
        self.campo_telefono.entry.insert(0, item.get("telefono", "") or "")
        self.campo_correo.entry.delete(0, "end")
        self.campo_correo.entry.insert(0, item.get("correo", "") or "")

        self._editando_id = item_id
        self.boton_guardar.configure(text="✓  Actualizar cliente")

    def _guardar_cliente(self):
        nombre = self.campo_nombre.entry.get().strip()
        cedula = self.campo_cedula.entry.get().strip()
        telefono = self.campo_telefono.entry.get().strip()
        correo = self.campo_correo.entry.get().strip()

        if not nombre or not cedula:
            messagebox.showwarning("Datos incompletos", "Nombre e identificación son obligatorios.")
            return

        if self._editando_id is not None:
            exito, mensaje, _ = actualizar_cliente(self._editando_id, nombre, cedula, telefono, correo)
        else:
            exito, mensaje, _ = crear_cliente(nombre, cedula, telefono, correo)

        if not exito:
            messagebox.showerror("Error al guardar", mensaje)
            return

        self._limpiar_formulario()
        self._refrescar()

    def _eliminar_seleccionado(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showinfo("Selecciona un cliente", "Selecciona una fila de la tabla para eliminar.")
            return

        item_id = int(seleccion[0])
        if not messagebox.askyesno("Confirmar eliminación", "¿Seguro que quieres eliminar este cliente?"):
            return

        exito, mensaje, _ = eliminar_cliente(item_id)
        if not exito:
            messagebox.showerror("Error al eliminar", mensaje)
            return

        if self._editando_id == item_id:
            self._limpiar_formulario()
        self._refrescar()
