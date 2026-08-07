"""Marco base para los módulos con formulario + tabla (CRUD).

Cada módulo (clientes, casos, expedientes, agenda, judicial) hereda de
`CrudFrame` y solo describe sus campos y cómo convertir sus datos. Toda la
mecánica común —crear, editar, eliminar, refrescar y filtrar— vive aquí.
"""

from tkinter import messagebox

import customtkinter as ctk

import api_client as api
import icons
from styles import (
    BG, DANGER, DANGER_HOVER, DISABLED, DISABLED_TEXT, INFO, INFO_HOVER,
    SUCCESS, SUCCESS_HOVER,
)
from ui_helpers import actualizar_tabla, combo, crear_tabla, entrada, tarjeta, titulo_seccion


class CrudFrame(ctk.CTkFrame):
    recurso = ""            # nombre del endpoint, p.ej. "clientes"
    pk = ""                 # nombre de la llave primaria, p.ej. "id_cliente"
    titulo = ""
    subtitulo = ""
    titulo_tabla = ""
    columnas = ()
    columnas_form = 4       # columnas del grid del formulario
    texto_crear = "Guardar"
    texto_actualizar = "Actualizar"

    def __init__(self, master):
        super().__init__(master, fg_color=BG, corner_radius=0)
        self._editando_id = None
        self._datos = []
        self._campos = {}
        self._fila_botones = 0
        self._construir()
        self.refrescar()

    # -- construcción de la interfaz ----------------------------------
    def _construir(self):
        titulo_seccion(self, self.titulo, self.subtitulo)

        form = tarjeta(self)
        form.pack(fill="x", pady=(0, 16))
        for i in range(self.columnas_form):
            form.grid_columnconfigure(i, weight=1)

        self.definir_campos(form)

        botones = ctk.CTkFrame(form, fg_color="transparent")
        botones.grid(row=self._fila_botones, column=0, columnspan=self.columnas_form,
                     sticky="e", padx=16, pady=(4, 16))
        self._boton_eliminar = ctk.CTkButton(
            botones, text="Eliminar", image=icons.imagen("eliminar", 15, "white"),
            compound="left", width=120, corner_radius=8,
            fg_color=DANGER, hover_color=DANGER_HOVER, command=self._al_eliminar)
        self._boton_eliminar.pack(side="left", padx=5)
        self._boton_editar = ctk.CTkButton(
            botones, text="Editar", image=icons.imagen("editar", 15, "white"),
            compound="left", width=110, corner_radius=8,
            fg_color=INFO, hover_color=INFO_HOVER, command=self._al_editar)
        self._boton_editar.pack(side="left", padx=5)
        self._icono_agregar = icons.imagen("agregar", 16, "white")
        self._icono_check = icons.imagen("check", 16, "white")
        self._boton_guardar = ctk.CTkButton(
            botones, text=self.texto_crear, image=self._icono_agregar,
            compound="left", width=170, corner_radius=8,
            fg_color=SUCCESS, hover_color=SUCCESS_HOVER, command=self._al_guardar)
        self._boton_guardar.pack(side="left", padx=5)
        self._deshabilitar_seleccion()

        card = tarjeta(self, self.titulo_tabla)
        card.pack(fill="both", expand=True)
        self.tabla = crear_tabla(card, self.columnas, [], 10)
        self.tabla.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        self.tabla.bind("<Double-1>", lambda _e: self._al_editar())
        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar)

    # -- estado habilitado/deshabilitado de Editar y Eliminar ---------
    def _habilitar_seleccion(self):
        self._boton_eliminar.configure(state="normal", fg_color=DANGER, hover_color=DANGER_HOVER, text_color="white")
        self._boton_editar.configure(state="normal", fg_color=INFO, hover_color=INFO_HOVER, text_color="white")

    def _deshabilitar_seleccion(self):
        self._boton_eliminar.configure(state="disabled", fg_color=DISABLED, text_color=DISABLED_TEXT)
        self._boton_editar.configure(state="disabled", fg_color=DISABLED, text_color=DISABLED_TEXT)

    def _al_seleccionar(self, _evento=None):
        if self.tabla.selection():
            self._habilitar_seleccion()
        else:
            self._deshabilitar_seleccion()
            self._limpiar()

    def campo(self, form, clave, etiqueta, placeholder, fila, columna, tipo="libre", columnspan=1, estado="normal"):
        """Agrega una entrada de texto al formulario y la registra por su clave."""
        contenedor = entrada(form, etiqueta, placeholder, tipo, estado=estado)
        return self._colocar(contenedor, clave, fila, columna, columnspan)

    def desplegable(self, form, clave, etiqueta, opciones, fila, columna, con_placeholder=False, columnspan=1):
        """Agrega un menú desplegable (combobox) al formulario."""
        contenedor = combo(form, etiqueta, opciones, con_placeholder=con_placeholder)
        return self._colocar(contenedor, clave, fila, columna, columnspan)

    def _colocar(self, contenedor, clave, fila, columna, columnspan):
        contenedor.grid(row=fila, column=columna, columnspan=columnspan,
                        sticky="ew", padx=16, pady=(8, 10))
        self._campos[clave] = contenedor
        self._fila_botones = max(self._fila_botones, fila + 1)
        return contenedor

    # -- utilidades para las subclases --------------------------------
    def valores(self):
        return {clave: c.obtener() for clave, c in self._campos.items()}

    def poner(self, clave, valor):
        self._campos[clave].asignar(valor)

    def opciones(self, clave, lista):
        """Actualiza las opciones de un desplegable (p.ej. clientes/casos)."""
        self._campos[clave].set_opciones(lista)

    # -- acciones -----------------------------------------------------
    def refrescar(self):
        self._datos = api.listar(self.recurso)
        self._pintar(self._datos)

    def filtrar(self, texto):
        texto = texto.strip().lower()
        if not texto:
            self._pintar(self._datos)
            return
        coincidencias = [r for r in self._datos
                         if any(texto in str(c).lower() for c in self.a_fila(r))]
        self._pintar(coincidencias)

    def _pintar(self, registros):
        filas = [self.a_fila(r) for r in registros]
        ids = [r[self.pk] for r in registros]
        actualizar_tabla(self.tabla, filas, ids)
        self._deshabilitar_seleccion()

    def _al_guardar(self):
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

        if self._editando_id is None:
            ok, mensaje, _ = api.crear(self.recurso, cuerpo)
        else:
            ok, mensaje, _ = api.actualizar(self.recurso, self._editando_id, cuerpo)

        if not ok:
            messagebox.showerror("No se pudo guardar", mensaje)
            return
        self._limpiar()
        self.refrescar()

    def _al_editar(self):
        registro = self._seleccion()
        if registro is None:
            return
        self.llenar_formulario(registro)
        self._editando_id = registro[self.pk]
        self._boton_guardar.configure(text=self.texto_actualizar, image=self._icono_check)

    def _al_eliminar(self):
        registro = self._seleccion()
        if registro is None:
            return
        if not messagebox.askyesno("Confirmar eliminación",
                                   "¿Seguro que quieres eliminar este registro?"):
            return
        ok, mensaje, _ = api.eliminar(self.recurso, registro[self.pk])
        if not ok:
            messagebox.showerror("No se pudo eliminar", mensaje)
            return
        if self._editando_id == registro[self.pk]:
            self._limpiar()
        self.refrescar()

    def _seleccion(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showinfo("Selecciona una fila", "Primero elige una fila de la tabla.")
            return None
        item_id = int(seleccion[0])
        return next((r for r in self._datos if r[self.pk] == item_id), None)

    def _limpiar(self):
        for contenedor in self._campos.values():
            contenedor.limpiar()
        self._editando_id = None
        self._boton_guardar.configure(text=self.texto_crear, image=self._icono_agregar)

    # -- a implementar por cada módulo --------------------------------
    def definir_campos(self, form):
        raise NotImplementedError

    def a_fila(self, registro):
        raise NotImplementedError

    def a_cuerpo(self, valores):
        raise NotImplementedError

    def llenar_formulario(self, registro):
        raise NotImplementedError

    def validar(self, valores):
        return None
