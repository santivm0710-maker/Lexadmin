from tkinter import messagebox

import customtkinter as ctk

from api_client import (
    actualizar_caso,
    buscar_id_cliente_por_nombre,
    crear_caso,
    eliminar_caso,
    obtener_casos,
    obtener_casos_raw,
    obtener_clientes_raw,
)
from styles import BG, SUCCESS, INFO, DANGER
from ui_helpers import titulo_seccion, tarjeta, crear_tabla, entrada, actualizar_tabla


class CasosFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG, corner_radius=0)
        self._editando_id = None
        self._crear_contenido()

    def _crear_contenido(self):
        titulo_seccion(self, "Gestión de Casos Legales", "Creación, actualización y seguimiento visual de expedientes jurídicos.")
        form = tarjeta(self)
        form.pack(fill="x", pady=(0, 16))
        for i in range(3):
            form.grid_columnconfigure(i, weight=1)

        self.campo_cliente = entrada(form, "Cliente asociado", "Nombre exacto del cliente registrado")
        self.campo_cliente.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 12))
        self.campo_expediente = entrada(form, "Número expediente", "Debe ser único")
        self.campo_expediente.grid(row=0, column=1, sticky="ew", padx=16, pady=(14, 12))
        self.campo_tipo = entrada(form, "Tipo de proceso", "Civil, laboral, familia...")
        self.campo_tipo.grid(row=0, column=2, sticky="ew", padx=16, pady=(14, 12))
        self.campo_estado = entrada(form, "Estado", "Activo / En revisión")
        self.campo_estado.grid(row=1, column=0, sticky="ew", padx=16, pady=(14, 12))
        self.campo_prioridad = entrada(form, "Prioridad", "Alta / Urgente")
        self.campo_prioridad.grid(row=1, column=1, sticky="ew", padx=16, pady=(14, 12))
        self.campo_abogado = entrada(form, "Abogado responsable", "Lic. responsable")
        self.campo_abogado.grid(row=1, column=2, sticky="ew", padx=16, pady=(14, 12))

        botones = ctk.CTkFrame(form, fg_color="transparent")
        botones.grid(row=2, column=0, columnspan=3, sticky="e", padx=16, pady=(0, 16))
        ctk.CTkButton(botones, text="Eliminar seleccionado", fg_color=DANGER, hover_color=DANGER, command=self._eliminar_seleccionado).pack(side="left", padx=5)
        ctk.CTkButton(botones, text="Editar seleccionado", fg_color=INFO, hover_color=INFO, command=self._cargar_seleccionado).pack(side="left", padx=5)
        self.boton_guardar = ctk.CTkButton(botones, text="Crear caso", fg_color=SUCCESS, hover_color=SUCCESS, command=self._guardar_caso)
        self.boton_guardar.pack(side="left", padx=5)

        card = tarjeta(self, "Casos registrados")
        card.pack(fill="both", expand=True)
        self._datos = obtener_casos_raw()
        ids = [item.get("id_caso") for item in self._datos]
        self.tabla = crear_tabla(card, ("Expediente", "Cliente", "Tipo", "Estado", "Prioridad", "Responsable"), obtener_casos(), 10, ids)
        self.tabla.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    def _refrescar(self):
        self._datos = obtener_casos_raw()
        ids = [item.get("id_caso") for item in self._datos]
        actualizar_tabla(self.tabla, obtener_casos(), ids)

    def _limpiar_formulario(self):
        for campo in (self.campo_cliente, self.campo_expediente, self.campo_tipo, self.campo_estado, self.campo_prioridad, self.campo_abogado):
            campo.entry.delete(0, "end")
        self._editando_id = None
        self.boton_guardar.configure(text="Crear caso")

    def _cargar_seleccionado(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showinfo("Selecciona un caso", "Selecciona una fila de la tabla para editar.")
            return

        item_id = int(seleccion[0])
        item = next((d for d in self._datos if d.get("id_caso") == item_id), None)
        if item is None:
            return

        nombres_por_id = {c.get("id_cliente"): c.get("nombre", "") for c in obtener_clientes_raw()}

        self.campo_cliente.entry.delete(0, "end")
        self.campo_cliente.entry.insert(0, nombres_por_id.get(item.get("id_cliente"), ""))
        self.campo_expediente.entry.delete(0, "end")
        self.campo_expediente.entry.insert(0, item.get("numero_expediente", ""))
        self.campo_tipo.entry.delete(0, "end")
        self.campo_tipo.entry.insert(0, item.get("tipo_caso", ""))
        self.campo_estado.entry.delete(0, "end")
        self.campo_estado.entry.insert(0, item.get("estado", ""))
        self.campo_prioridad.entry.delete(0, "end")
        self.campo_prioridad.entry.insert(0, item.get("prioridad", ""))
        self.campo_abogado.entry.delete(0, "end")
        self.campo_abogado.entry.insert(0, item.get("abogado_responsable", "") or "")

        self._editando_id = item_id
        self.boton_guardar.configure(text="Actualizar caso")

    def _guardar_caso(self):
        cliente = self.campo_cliente.entry.get().strip()
        expediente = self.campo_expediente.entry.get().strip()
        tipo = self.campo_tipo.entry.get().strip()
        estado = self.campo_estado.entry.get().strip()
        prioridad = self.campo_prioridad.entry.get().strip()
        abogado = self.campo_abogado.entry.get().strip()

        if not cliente or not expediente or not tipo or not estado or not prioridad:
            messagebox.showwarning("Datos incompletos", "Cliente, expediente, tipo, estado y prioridad son obligatorios.")
            return

        id_cliente = buscar_id_cliente_por_nombre(cliente)
        if id_cliente is None:
            messagebox.showerror("Cliente no encontrado", f"No existe un cliente registrado con el nombre '{cliente}'.")
            return

        if self._editando_id is not None:
            exito, mensaje, _ = actualizar_caso(self._editando_id, expediente, id_cliente, tipo, estado, prioridad, abogado)
        else:
            exito, mensaje, _ = crear_caso(expediente, id_cliente, tipo, estado, prioridad, abogado)

        if not exito:
            messagebox.showerror("Error al guardar", mensaje)
            return

        self._limpiar_formulario()
        self._refrescar()

    def _eliminar_seleccionado(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showinfo("Selecciona un caso", "Selecciona una fila de la tabla para eliminar.")
            return

        item_id = int(seleccion[0])
        if not messagebox.askyesno("Confirmar eliminación", "¿Seguro que quieres eliminar este caso?"):
            return

        exito, mensaje, _ = eliminar_caso(item_id)
        if not exito:
            messagebox.showerror("Error al eliminar", mensaje)
            return

        if self._editando_id == item_id:
            self._limpiar_formulario()
        self._refrescar()
