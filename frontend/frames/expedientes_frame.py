import os
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk
"""a"""
import api_client as api
from crud_frame import CrudFrame
from ui_helpers import formatear_fecha

TIPOS_DOCUMENTO = ["Expediente", "Prueba", "Resolución", "Contrato", "Escrito", "Otro"]
ESTADOS_OCR = ["Pendiente", "Procesado"]


class ExpedientesFrame(CrudFrame):
    recurso = "expedientes"
    pk = "id_expediente"
    titulo = "Digitalización y Expedientes"
    subtitulo = "Documentos por caso, con su tipo y estado de digitalización (OCR)."
    titulo_tabla = "Documentos digitalizados"
    columnas = ("Cliente", "Caso", "Documento", "Tipo", "OCR", "Subido")
    columnas_form = 5
    texto_crear = "Subir documento"
    texto_actualizar = "Actualizar documento"

    def __init__(self, master):
        self._archivo_pdf_seleccionado = None
        self._ruta_pdf_existente = None
        super().__init__(master)

    def definir_campos(self, form):
        """Define los campos del formulario para crear o editar un expediente."""
        self.desplegable(form, "caso", "Caso (expediente)", [], 0, 0, con_placeholder=True)
        self.campo(form, "nombre_documento", "Documento", "archivo.pdf", 0, 1, estado="readonly")
        self.desplegable(form, "tipo_documento", "Tipo de documento", TIPOS_DOCUMENTO, 0, 2)
        self.desplegable(form, "estado_ocr", "Estado OCR", ESTADOS_OCR, 0, 3)
        self._boton_pdf = ctk.CTkButton(
            form,
            text="Seleccionar PDF",
            width=140,
            corner_radius=8,
            command=self._seleccionar_pdf,
        )
        self._boton_pdf.grid(row=0, column=4, sticky="ew", padx=16, pady=(8, 10))
        self._boton_abrir = ctk.CTkButton(
            form,
            text="Abrir PDF",
            width=120,
            corner_radius=8,
            command=self._abrir_pdf,
            state="disabled",
        )
        self._boton_abrir.grid(row=0, column=5, sticky="ew", padx=16, pady=(8, 10))

    def refrescar(self):
        self._clientes = {c["id_cliente"]: c["nombre_completo"] for c in api.listar("clientes")}
        self._casos = {c["id_caso"]: c for c in api.listar("casos")}
        self.opciones("caso", [c["numero_expediente"] for c in self._casos.values()])
        super().refrescar()

    def valores(self):
        valores = super().valores()
        valores["archivo_pdf"] = self._archivo_pdf_seleccionado
        return valores

    def _seleccionar_pdf(self):
        """Abre un selector de archivos para elegir el PDF que se va a subir."""
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo PDF",
            filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")],
        )
        if not ruta:
            return
        self._archivo_pdf_seleccionado = ruta
        self._ruta_pdf_existente = None
        self.poner("nombre_documento", Path(ruta).name)
        self._boton_abrir.configure(state="normal")

    def _abrir_pdf(self):
        ruta = self._archivo_pdf_seleccionado or self._ruta_pdf_existente
        if not ruta or not os.path.exists(ruta):
            messagebox.showinfo("Abrir PDF", "No hay un archivo PDF válido para abrir.")
            return
        try:
            os.startfile(ruta)
        except OSError:
            messagebox.showerror("No se pudo abrir", "No se pudo abrir el archivo PDF seleccionado.")

    def _al_guardar(self):
        """Guarda el expediente y envía el PDF al backend si fue seleccionado."""
        valores = self.valores()
        error = self.validar(valores)
        if error:
            messagebox.showwarning("Datos incompletos", error)
            return
        try:
            cuerpo = self.a_cuerpo(valores)
        except ValueError as e:
            messagebox.showerror("Revisa los datos", str(e))
            return

        archivo_pdf = valores.get("archivo_pdf")
        if self._editando_id is None:
            ok, mensaje, _ = api.crear_con_archivo(self.recurso, cuerpo, archivo_pdf)
        else:
            ok, mensaje, _ = api.actualizar_con_archivo(self.recurso, self._editando_id, cuerpo, archivo_pdf)

        if not ok:
            messagebox.showerror("No se pudo guardar", mensaje)
            return
        self._limpiar()
        self.refrescar()

    def _limpiar(self):
        super()._limpiar()
        self._archivo_pdf_seleccionado = None
        self._ruta_pdf_existente = None
        if hasattr(self, "_boton_abrir"):
            self._boton_abrir.configure(state="disabled")

    def a_fila(self, r):
        caso = self._casos.get(r["id_caso"], {})
        return (self._clientes.get(r["id_cliente"], "?"), caso.get("numero_expediente", "?"),
                r.get("nombre_documento") or "", r.get("tipo_documento") or "",
                r.get("estado_ocr") or "", formatear_fecha(r.get("fecha_subida")))

    def validar(self, v):
        if not v["caso"]:
            return "Debes elegir un caso. Si no aparece, créalo primero en Casos."
        if not v["nombre_documento"]:
            return "El nombre del documento es obligatorio."
        if self._editando_id is None and not v.get("archivo_pdf"):
            return "Debes seleccionar un archivo PDF para crear el expediente."
        return None

    def a_cuerpo(self, v):
        caso = api.buscar_caso_por_expediente(v["caso"])
        if caso is None:
            raise ValueError(f"No existe un caso con expediente '{v['caso']}'.")
        return {
            "id_cliente": caso["id_cliente"],
            "id_caso": caso["id_caso"],
            "nombre_documento": v["nombre_documento"],
            "tipo_documento": v["tipo_documento"] or None,
            "estado_ocr": v["estado_ocr"] or "Pendiente",
        }

    def llenar_formulario(self, r):
        caso = self._casos.get(r["id_caso"], {})
        self.poner("caso", caso.get("numero_expediente"))
        self.poner("nombre_documento", r.get("nombre_documento"))
        self.poner("tipo_documento", r.get("tipo_documento"))
        self.poner("estado_ocr", r.get("estado_ocr"))
        self._archivo_pdf_seleccionado = None
        self._ruta_pdf_existente = r.get("ruta_pdf")
        if hasattr(self, "_boton_abrir"):
            self._boton_abrir.configure(state="normal" if self._ruta_pdf_existente else "disabled")
