from tkinter import messagebox

import customtkinter as ctk

from api_client import (
    actualizar_info_judicial,
    buscar_id_caso_por_expediente,
    crear_info_judicial,
    eliminar_info_judicial,
    obtener_casos_raw,
    obtener_judicial,
    obtener_judicial_raw,
)
from styles import BG, SUCCESS, INFO, DANGER
from ui_helpers import titulo_seccion, tarjeta, crear_tabla, entrada, actualizar_tabla


class JudicialFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG, corner_radius=0)
        self._editando_id = None
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

        botones = ctk.CTkFrame(form, fg_color="transparent")
        botones.grid(row=1, column=0, columnspan=5, sticky="e", padx=12, pady=(0, 16))
        ctk.CTkButton(botones, text="Eliminar seleccionado", fg_color=DANGER, hover_color=DANGER, command=self._eliminar_seleccionado).pack(side="left", padx=5)
        ctk.CTkButton(botones, text="Editar seleccionado", fg_color=INFO, hover_color=INFO, command=self._cargar_seleccionado).pack(side="left", padx=5)
        self.boton_guardar = ctk.CTkButton(botones, text="Guardar datos", fg_color=SUCCESS, hover_color=SUCCESS, command=self._guardar_datos)
        self.boton_guardar.pack(side="left", padx=5)

        card = tarjeta(self, "Información judicial registrada")
        card.pack(fill="both", expand=True)
        self._datos = obtener_judicial_raw()
        ids = [item.get("id_info_judicial") for item in self._datos]
        self.tabla = crear_tabla(card, ("Caso", "Juzgado", "Juez", "Fiscal", "Contacto"), obtener_judicial(), 10, ids)
        self.tabla.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    def _refrescar(self):
        self._datos = obtener_judicial_raw()
        ids = [item.get("id_info_judicial") for item in self._datos]
        actualizar_tabla(self.tabla, obtener_judicial(), ids)

    def _limpiar_formulario(self):
        for campo in (self.campo_caso, self.campo_juzgado, self.campo_juez, self.campo_fiscal, self.campo_contacto):
            campo.entry.delete(0, "end")
        self._editando_id = None
        self.boton_guardar.configure(text="Guardar datos")

    def _cargar_seleccionado(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showinfo("Selecciona un registro", "Selecciona una fila de la tabla para editar.")
            return

        item_id = int(seleccion[0])
        item = next((d for d in self._datos if d.get("id_info_judicial") == item_id), None)
        if item is None:
            return

        expedientes_por_id = {c.get("id_caso"): c.get("numero_expediente", "") for c in obtener_casos_raw()}

        self.campo_caso.entry.delete(0, "end")
        self.campo_caso.entry.insert(0, expedientes_por_id.get(item.get("id_caso"), ""))
        self.campo_juzgado.entry.delete(0, "end")
        self.campo_juzgado.entry.insert(0, item.get("juzgado", ""))
        self.campo_juez.entry.delete(0, "end")
        self.campo_juez.entry.insert(0, item.get("juez", "") or "")
        self.campo_fiscal.entry.delete(0, "end")
        self.campo_fiscal.entry.insert(0, item.get("fiscal", "") or "")
        self.campo_contacto.entry.delete(0, "end")
        self.campo_contacto.entry.insert(0, item.get("contacto_institucional", "") or "")

        self._editando_id = item_id
        self.boton_guardar.configure(text="Actualizar datos")

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

        if self._editando_id is not None:
            exito, mensaje, _ = actualizar_info_judicial(self._editando_id, id_caso, juzgado, juez, fiscal, contacto)
        else:
            exito, mensaje, _ = crear_info_judicial(id_caso, juzgado, juez, fiscal, contacto)

        if not exito:
            messagebox.showerror("Error al guardar", mensaje)
            return

        self._limpiar_formulario()
        self._refrescar()

    def _eliminar_seleccionado(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showinfo("Selecciona un registro", "Selecciona una fila de la tabla para eliminar.")
            return

        item_id = int(seleccion[0])
        if not messagebox.askyesno("Confirmar eliminación", "¿Seguro que quieres eliminar este registro?"):
            return

        exito, mensaje, _ = eliminar_info_judicial(item_id)
        if not exito:
            messagebox.showerror("Error al eliminar", mensaje)
            return

        if self._editando_id == item_id:
            self._limpiar_formulario()
        self._refrescar()
