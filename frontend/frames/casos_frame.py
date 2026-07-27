from tkinter import messagebox

import customtkinter as ctk

from api_client import buscar_id_cliente_por_nombre, crear_caso, obtener_casos
from styles import BG, SUCCESS
from ui_helpers import titulo_seccion, tarjeta, crear_tabla, entrada, actualizar_tabla


class CasosFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG, corner_radius=0)
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

        ctk.CTkButton(form, text="Crear caso", fg_color=SUCCESS, hover_color=SUCCESS, command=self._crear_caso).grid(row=2, column=2, sticky="e", padx=16, pady=(0, 16))

        card = tarjeta(self, "Casos registrados")
        card.pack(fill="both", expand=True)
        self.tabla = crear_tabla(card, ("Expediente", "Cliente", "Tipo", "Estado", "Prioridad", "Responsable"), obtener_casos(), 10)
        self.tabla.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    def _crear_caso(self):
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

        exito, mensaje, _ = crear_caso(expediente, id_cliente, tipo, estado, prioridad, abogado)
        if not exito:
            messagebox.showerror("Error al guardar", mensaje)
            return

        for campo in (self.campo_cliente, self.campo_expediente, self.campo_tipo, self.campo_estado, self.campo_prioridad, self.campo_abogado):
            campo.entry.delete(0, "end")
        actualizar_tabla(self.tabla, obtener_casos())
