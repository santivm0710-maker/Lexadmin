from tkinter import messagebox

import customtkinter as ctk

from api_client import buscar_id_caso_por_expediente, crear_expediente, obtener_expedientes
from styles import BG, SUCCESS
from ui_helpers import titulo_seccion, tarjeta, crear_tabla, entrada, actualizar_tabla


class ExpedientesFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG, corner_radius=0)
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

        ctk.CTkButton(form, text="Subir PDF", fg_color=SUCCESS, hover_color=SUCCESS, command=self._subir_documento).grid(row=1, column=3, sticky="e", padx=16, pady=(0, 16))

        card = tarjeta(self, "Documentos digitalizados")
        card.pack(fill="both", expand=True)
        self.tabla = crear_tabla(card, ("Cliente", "Caso", "Archivo", "Tipo", "OCR", "Estructura"), obtener_expedientes(), 10)
        self.tabla.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    def _subir_documento(self):
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

        exito, mensaje, _ = crear_expediente(id_caso, documento, tipo)
        if not exito:
            messagebox.showerror("Error al guardar", mensaje)
            return

        for campo in (self.campo_caso, self.campo_documento, self.campo_tipo):
            campo.entry.delete(0, "end")
        actualizar_tabla(self.tabla, obtener_expedientes())
