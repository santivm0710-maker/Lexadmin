import customtkinter as ctk

from api_client import obtener_clientes
from styles import BG, SUCCESS, INFO
from ui_helpers import titulo_seccion, tarjeta, crear_tabla, entrada


class ClientesFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG, corner_radius=0)
        self._crear_contenido()

    def _crear_contenido(self):
        titulo_seccion(self, "Gestión de Clientes", "Registro visual, consulta e historial asociado a casos legales.")
        campos = [("Nombre completo", "Ej. Juan Pérez"), ("Identificación", "Ej. 1-1111-1111"), ("Teléfono", "Ej. 8888-1234"), ("Correo", "cliente@email.com")]
        self._crear_formulario(campos, "Guardar cliente", "Buscar cliente")
        self._crear_tabla(("Cliente", "Identificación", "Teléfono", "Correo", "Caso asociado"), obtener_clientes())

    def _crear_formulario(self, campos, texto_boton1, texto_boton2):
        form = tarjeta(self)
        form.pack(fill="x", pady=(0, 16))
        for i in range(4):
            form.grid_columnconfigure(i, weight=1)
        for i, (label, ph) in enumerate(campos):
            entrada(form, label, ph).grid(row=0, column=i, sticky="ew", padx=16, pady=(14, 16))
        botones = ctk.CTkFrame(form, fg_color="transparent")
        botones.grid(row=1, column=0, columnspan=4, sticky="e", padx=16, pady=(0, 16))
        ctk.CTkButton(botones, text=texto_boton2, fg_color=INFO, hover_color=INFO, command=lambda: None).pack(side="left", padx=5)
        ctk.CTkButton(botones, text=texto_boton1, fg_color=SUCCESS, hover_color=SUCCESS, command=lambda: None).pack(side="left", padx=5)

    def _crear_tabla(self, columnas, filas):
        card = tarjeta(self, "Clientes registrados")
        card.pack(fill="both", expand=True)
        tabla = crear_tabla(card, columnas, filas, 10)
        tabla.pack(fill="both", expand=True, padx=18, pady=(0, 18))
