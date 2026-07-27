from tkinter import messagebox

import customtkinter as ctk

from api_client import (
    actualizar_expediente,
    buscar_id_caso_por_expediente,
    crear_expediente,
    eliminar_expediente,
    obtener_casos_raw,
    obtener_expedientes,
    obtener_expedientes_raw,
)
from styles import BG, SUCCESS, INFO, DANGER
from ui_helpers import titulo_seccion, tarjeta, crear_tabla, entrada, actualizar_tabla


class ExpedientesFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG, corner_radius=0)
        self._editando_id = None
        self._crear_contenido()

    def _crear_contenido(self):
        titulo_seccion(self, "Digitalización y Expedientes", "Carga visual de PDF, OCR pendiente y organización Cliente → Caso → Documento.")
        form = tarjeta(self)
        form.pack(fill="x", pady=(0, 16))
        for i in range(4):
            form.grid_columnconfigure(i, weight=1)

        self.campo_caso = entrada(form, "Caso", "# expediente")
        self.campo_caso.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 16))
        self.campo_documento = entrada(form, "Documento PDF", "archivo.pdf")
        self.campo_documento.grid(row=0, column=1, sticky="ew", padx=16, pady=(14, 16))
        self.campo_tipo = entrada(form, "Tipo documento", "Expediente / Prueba")
        self.campo_tipo.grid(row=0, column=2, sticky="ew", padx=16, pady=(14, 16))

        botones = ctk.CTkFrame(form, fg_color="transparent")
        botones.grid(row=1, column=0, columnspan=4, sticky="e", padx=16, pady=(0, 16))
        ctk.CTkButton(botones, text="Eliminar seleccionado", fg_color=DANGER, hover_color=DANGER, command=self._eliminar_seleccionado).pack(side="left", padx=5)
        ctk.CTkButton(botones, text="✎  Editar seleccionado", fg_color=INFO, hover_color=INFO, command=self._cargar_seleccionado).pack(side="left", padx=5)
        self.boton_guardar = ctk.CTkButton(botones, text="＋  Subir PDF", fg_color=SUCCESS, hover_color=SUCCESS, command=self._guardar_documento)
        self.boton_guardar.pack(side="left", padx=5)

        card = tarjeta(self, "Documentos digitalizados")
        card.pack(fill="both", expand=True)
        self._datos = obtener_expedientes_raw()
        ids = [item.get("id_expediente") for item in self._datos]
        self.tabla = crear_tabla(card, ("Cliente", "Caso", "Archivo", "Tipo", "OCR", "Estructura"), obtener_expedientes(), 10, ids)
        self.tabla.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    def _refrescar(self):
        self._datos = obtener_expedientes_raw()
        ids = [item.get("id_expediente") for item in self._datos]
        actualizar_tabla(self.tabla, obtener_expedientes(), ids)

    def _limpiar_formulario(self):
        for campo in (self.campo_caso, self.campo_documento, self.campo_tipo):
            campo.entry.delete(0, "end")
        self._editando_id = None
        self.boton_guardar.configure(text="＋  Subir PDF")

    def _cargar_seleccionado(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showinfo("Selecciona un expediente", "Selecciona una fila de la tabla para editar.")
            return

        item_id = int(seleccion[0])
        item = next((d for d in self._datos if d.get("id_expediente") == item_id), None)
        if item is None:
            return

        expedientes_por_id = {c.get("id_caso"): c.get("numero_expediente", "") for c in obtener_casos_raw()}

        self.campo_caso.entry.delete(0, "end")
        self.campo_caso.entry.insert(0, expedientes_por_id.get(item.get("id_caso"), ""))
        self.campo_documento.entry.delete(0, "end")
        self.campo_documento.entry.insert(0, item.get("nombre_documento", ""))
        self.campo_tipo.entry.delete(0, "end")
        self.campo_tipo.entry.insert(0, item.get("tipo_documento", ""))

        self._editando_id = item_id
        self.boton_guardar.configure(text="✓  Actualizar documento")

    def _guardar_documento(self):
        caso = self.campo_caso.entry.get().strip()
        documento = self.campo_documento.entry.get().strip()
        tipo = self.campo_tipo.entry.get().strip()

        if not caso or not documento or not tipo:
            messagebox.showwarning("Datos incompletos", "Caso, documento y tipo son obligatorios.")
            return

        id_caso = buscar_id_caso_por_expediente(caso)
        if id_caso is None:
            messagebox.showerror("Caso no encontrado", f"No existe un caso registrado con el expediente '{caso}'.")
            return

        if self._editando_id is not None:
            exito, mensaje, _ = actualizar_expediente(self._editando_id, id_caso, documento, tipo)
        else:
            exito, mensaje, _ = crear_expediente(id_caso, documento, tipo)

        if not exito:
            messagebox.showerror("Error al guardar", mensaje)
            return

        self._limpiar_formulario()
        self._refrescar()

    def _eliminar_seleccionado(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showinfo("Selecciona un expediente", "Selecciona una fila de la tabla para eliminar.")
            return

        item_id = int(seleccion[0])
        if not messagebox.askyesno("Confirmar eliminación", "¿Seguro que quieres eliminar este expediente?"):
            return

        exito, mensaje, _ = eliminar_expediente(item_id)
        if not exito:
            messagebox.showerror("Error al eliminar", mensaje)
            return

        if self._editando_id == item_id:
            self._limpiar_formulario()
        self._refrescar()
