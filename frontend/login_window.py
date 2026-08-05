"""Ventana de acceso: inicio de sesión y creación de cuenta.

Se muestra antes que `LegalDeskApp`. Al autenticar correctamente deja el
usuario en `self.usuario` y se cierra; `main.py` decide qué hacer después.

El diseño repite la identidad de la aplicación principal: panel lateral
navy con la marca dorada a la izquierda y el formulario a la derecha, con
los mismos tokens de color, tipografía e iconografía que el resto del
sistema.
"""

import customtkinter as ctk

import api_client
import icons
from styles import (
    ACCENT, BG, BORDER, CARD, DANGER, DANGER_BG, DISABLED, DISABLED_TEXT, FONT_FAMILY,
    FONT_SERIF, MUTED, PRIMARY, PRIMARY_HOVER, ROW_ALT, SIDEBAR, SIDEBAR_HOVER,
    SIDEBAR_TEXT, SUCCESS, SUCCESS_BG, TEXT, configurar_tema,
)
from ui_helpers import entrada, insignia_marca, validar_email

ANCHO, ALTO = 900, 640
ANCHO_MARCA = 340
ANCHO_FORM = 356

VENTAJAS = [
    ("clientes", "Clientes y expedientes centralizados"),
    ("casos", "Casos y audiencias con seguimiento"),
    ("escudo", "Acceso seguro con tu propia cuenta"),
]


class LoginWindow(ctk.CTk):
    def __init__(self):
        configurar_tema()
        super().__init__()
        icons.imagen.cache_clear()  # los íconos cacheados pertenecían a una raíz de Tk ya destruida
        self.title("LexAdmin | Acceso")
        self._centrar(ANCHO, ALTO)
        self.resizable(False, False)
        self.configure(fg_color=BG)

        self.usuario = None
        self._modo_registro = False
        self._campos = {}
        self._errores = {}

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._crear_panel_marca()

        self.panel_form = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self.panel_form.grid(row=0, column=1, sticky="nsew")

        self.bind("<Return>", lambda _e: self._enviar())
        self._dibujar_formulario()

    def _centrar(self, ancho, alto):
        x = (self.winfo_screenwidth() - ancho) // 2
        y = (self.winfo_screenheight() - alto) // 2
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    # ------------------------------------------------------------------
    # Panel de marca (se construye una sola vez)
    # ------------------------------------------------------------------
    def _crear_panel_marca(self):
        panel = ctk.CTkFrame(self, width=ANCHO_MARCA, fg_color=SIDEBAR, corner_radius=0)
        panel.grid(row=0, column=0, sticky="nsew")
        panel.grid_propagate(False)

        marca = ctk.CTkFrame(panel, fg_color="transparent")
        marca.pack(anchor="w", padx=38, pady=(54, 0))
        insignia_marca(marca, 46, 22).pack(anchor="w")
        ctk.CTkLabel(marca, text="LexAdmin", text_color="white",
                     font=ctk.CTkFont(family=FONT_SERIF, size=29, weight="bold")).pack(anchor="w", pady=(14, 0))
        ctk.CTkLabel(marca, text="Gestión de despacho legal", text_color=SIDEBAR_TEXT,
                     font=ctk.CTkFont(family=FONT_FAMILY, size=13)).pack(anchor="w", pady=(2, 0))

        ctk.CTkFrame(panel, width=46, height=3, fg_color=ACCENT, corner_radius=2).pack(anchor="w", padx=38, pady=(26, 0))

        lista = ctk.CTkFrame(panel, fg_color="transparent")
        lista.pack(anchor="w", padx=38, pady=(30, 0), fill="x")
        for nombre_icono, texto in VENTAJAS:
            fila = ctk.CTkFrame(lista, fg_color="transparent")
            fila.pack(anchor="w", fill="x", pady=9)
            ctk.CTkLabel(fila, text="", image=icons.imagen(nombre_icono, 17, ACCENT),
                         width=24).pack(side="left", anchor="n")
            ctk.CTkLabel(fila, text=texto, text_color=SIDEBAR_TEXT, justify="left", wraplength=236,
                         font=ctk.CTkFont(family=FONT_FAMILY, size=13)).pack(side="left", anchor="w")

        ctk.CTkFrame(panel, height=1, fg_color=SIDEBAR_HOVER).pack(side="bottom", fill="x", padx=38, pady=(0, 22))
        ctk.CTkLabel(panel, text="Acceso exclusivo para personal autorizado\ndel despacho.",
                     text_color="#7C87AC", justify="left",
                     font=ctk.CTkFont(family=FONT_FAMILY, size=11)).pack(side="bottom", anchor="w", padx=38, pady=(0, 12))

    # ------------------------------------------------------------------
    # Formulario (se redibuja al alternar entre acceso y registro)
    # ------------------------------------------------------------------
    def _dibujar_formulario(self):
        for widget in self.panel_form.winfo_children():
            widget.destroy()
        self._campos = {}
        self._errores = {}

        contenido = ctk.CTkFrame(self.panel_form, fg_color="transparent")
        contenido.place(relx=0.5, rely=0.5, anchor="center")
        # Espaciador que fija el ancho de la columna; el alto lo calcula el contenido.
        ctk.CTkFrame(contenido, width=ANCHO_FORM, height=1, fg_color="transparent").pack()

        registro = self._modo_registro
        ctk.CTkLabel(contenido, text="Crear cuenta" if registro else "Iniciar sesión", text_color=TEXT,
                     font=ctk.CTkFont(family=FONT_FAMILY, size=25, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(
            contenido, text_color=MUTED, justify="left", wraplength=ANCHO_FORM,
            text=("Completa tus datos para registrarte en el sistema."
                  if registro else "Ingresa tus credenciales para continuar."),
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
        ).pack(anchor="w", pady=(4, 22))

        if registro:
            self._campo(contenido, "nombre", "Nombre completo", tipo="texto")
            self._campo(contenido, "correo", "Correo electrónico")
            self._campo(contenido, "password", "Contraseña", password=True,
                        ayuda="Mínimo 6 caracteres.")
            self._campo(contenido, "confirmar", "Confirmar contraseña", password=True)
        else:
            self._campo(contenido, "correo", "Correo electrónico")
            self._campo(contenido, "password", "Contraseña", password=True)

        self.banner = ctk.CTkLabel(contenido, text="", corner_radius=8, anchor="w", justify="left",
                                   wraplength=330, font=ctk.CTkFont(family=FONT_FAMILY, size=12))
        self.banner.pack(fill="x", pady=(10, 0))
        self.banner.pack_forget()

        self._texto_boton = "Crear cuenta" if registro else "Iniciar sesión"
        self.boton = ctk.CTkButton(
            contenido, text=self._texto_boton, height=44, corner_radius=8,
            fg_color=PRIMARY, hover_color=PRIMARY_HOVER, text_color="white",
            font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
            command=self._enviar)
        self.boton.pack(fill="x", pady=(18, 14))

        pie = ctk.CTkFrame(contenido, fg_color="transparent")
        pie.pack()
        ctk.CTkLabel(pie, text="¿Ya tienes cuenta?" if registro else "¿No tienes cuenta?", text_color=MUTED,
                     font=ctk.CTkFont(family=FONT_FAMILY, size=13)).pack(side="left")
        ctk.CTkButton(pie, text="Iniciar sesión" if registro else "Crear cuenta",
                      fg_color="transparent", hover=False, text_color=ACCENT, width=10,
                      font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
                      command=self._alternar_modo).pack(side="left", padx=3)

        self._campos["nombre" if registro else "correo"].campo.focus_set()

    def _campo(self, parent, clave, etiqueta, tipo="libre", password=False, ayuda=None):
        """Etiqueta visible + campo + mensaje de error propio bajo el campo."""
        caja = ctk.CTkFrame(parent, fg_color="transparent")
        caja.pack(fill="x")

        campo = entrada(caja, etiqueta, "", tipo=tipo, mostrar="•" if password else "")
        campo.pack(fill="x")

        error = ctk.CTkLabel(caja, text=ayuda or "", text_color=MUTED, anchor="w", height=16,
                             font=ctk.CTkFont(family=FONT_FAMILY, size=11))
        error.pack(fill="x", pady=(3, 8))
        error._ayuda = ayuda  # texto neutro al que se vuelve cuando el campo es válido

        self._campos[clave] = campo
        self._errores[clave] = error

        if password:
            self._agregar_ojo(campo)
        # Validación al salir del campo, no solo al enviar (se suma al foco ya existente).
        campo.campo.bind("<FocusOut>", lambda _e, k=clave: self._validar(k), add="+")
        return campo

    def _agregar_ojo(self, campo):
        """Botón mostrar/ocultar contraseña dentro del propio campo."""
        estado = {"visible": False}
        boton = ctk.CTkButton(campo.campo, text="", width=28, height=28, corner_radius=6,
                              fg_color="transparent", hover_color=ROW_ALT,
                              image=icons.imagen("ver", 15, MUTED))

        def alternar():
            estado["visible"] = not estado["visible"]
            campo.campo.configure(show="" if estado["visible"] else "•")
            boton.configure(image=icons.imagen("ocultar" if estado["visible"] else "ver", 15, MUTED))

        boton.configure(command=alternar)
        boton.place(relx=1.0, rely=0.5, x=-6, anchor="e")

    # ------------------------------------------------------------------
    # Validación
    # ------------------------------------------------------------------
    def _marcar(self, clave, mensaje=""):
        etiqueta = self._errores.get(clave)
        if etiqueta is None:
            return True
        if mensaje:
            etiqueta.configure(text=mensaje, text_color=DANGER)
        else:
            etiqueta.configure(text=etiqueta._ayuda or "", text_color=MUTED)
        return not mensaje

    def _validar(self, clave):
        """Valida un campo concreto. Devuelve True si está correcto."""
        valor = self._campos[clave].obtener()
        if not valor:
            return self._marcar(clave)  # vacío no se marca hasta enviar

        if clave == "correo" and not validar_email(valor):
            return self._marcar(clave, "Ingresa un correo electrónico válido.")
        if clave == "password" and self._modo_registro and len(valor) < 6:
            return self._marcar(clave, "La contraseña debe tener al menos 6 caracteres.")
        if clave == "confirmar" and valor != self._campos["password"].obtener():
            return self._marcar(clave, "Las contraseñas no coinciden.")
        return self._marcar(clave)

    def _validar_todo(self):
        correcto = True
        for clave, campo in self._campos.items():
            if not campo.obtener():
                self._marcar(clave, "Este campo es obligatorio.")
                correcto = False
            elif not self._validar(clave):
                correcto = False
        return correcto

    # ------------------------------------------------------------------
    # Avisos generales
    # ------------------------------------------------------------------
    def _avisar(self, mensaje, exito=False):
        if not mensaje:
            self.banner.pack_forget()
            return
        self.banner.configure(text=f"  {mensaje}", fg_color=SUCCESS_BG if exito else DANGER_BG,
                              text_color=SUCCESS if exito else DANGER)
        self.banner.pack(fill="x", pady=(10, 0), before=self.boton)

    def _enviar(self):
        self._avisar("")
        if not self._validar_todo():
            return
        self.boton.configure(state="disabled", text="Verificando...",
                             fg_color=DISABLED, text_color=DISABLED_TEXT)
        self.update_idletasks()  # pinta el estado antes de la llamada, que bloquea la interfaz
        if self._modo_registro:
            self._registrar()
        else:
            self._acceder()

    def _restaurar_boton(self):
        self.boton.configure(state="normal", text=self._texto_boton,
                             fg_color=PRIMARY, text_color="white")

    def _acceder(self):
        ok, texto, data = api_client.iniciar_sesion({
            "correo": self._campos["correo"].obtener(),
            "password": self._campos["password"].obtener(),
        })
        if ok:
            self.usuario = data
            self.destroy()  # no hay que restaurar el botón: la ventana se va
        else:
            self._restaurar_boton()
            self._avisar(texto or "Correo o contraseña incorrectos.")

    def _registrar(self):
        ok, texto, _data = api_client.registrar_usuario({
            "nombre_completo": self._campos["nombre"].obtener(),
            "correo": self._campos["correo"].obtener(),
            "password": self._campos["password"].obtener(),
        })
        if ok:
            self._modo_registro = False
            self._dibujar_formulario()  # crea un botón nuevo, ya habilitado
            self._avisar("Cuenta creada. Ya puedes iniciar sesión.", exito=True)
        else:
            self._restaurar_boton()
            self._avisar(texto or "No se pudo crear la cuenta.")

    def _alternar_modo(self):
        self._modo_registro = not self._modo_registro
        self._dibujar_formulario()
