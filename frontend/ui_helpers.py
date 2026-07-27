"""Componentes visuales reutilizables y utilidades del frontend."""

import re
from datetime import datetime
from tkinter import ttk

import customtkinter as ctk

from styles import ACCENT, BORDER, CARD, FONT_FAMILY, MUTED, ROW_ALT, TEXT

# ------------------------------------------------------------------
# Validación de entradas (evita letras donde van números y viceversa)
# ------------------------------------------------------------------
_PATRONES = {
    "texto": r"[A-Za-zÁÉÍÓÚáéíóúÜüÑñ .]*",   # solo letras, espacios y punto
    "numero": r"[0-9]*",                       # solo dígitos
    "identificacion": r"[0-9\-]*",             # dígitos y guiones
    "telefono": r"[0-9+\-() ]*",               # dígitos y símbolos de teléfono
    "fecha": r"[0-9/]*",                        # dígitos y /
    "hora": r"[0-9:]*",                         # dígitos y :
}


def _crear_validador(widget, tipo):
    patron = _PATRONES.get(tipo)
    if patron is None:
        return None
    regex = re.compile(f"^{patron}$")
    return widget.register(lambda propuesto: bool(regex.match(propuesto)))


def validar_email(texto):
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", texto))


# ------------------------------------------------------------------
# Formato de fechas y horas que llegan del backend
# ------------------------------------------------------------------
def formatear_fecha(valor):
    """De 'YYYY-MM-DD' (o ISO) a 'dd/mm/aaaa'."""
    if not valor:
        return ""
    try:
        return datetime.fromisoformat(str(valor)).strftime("%d/%m/%Y")
    except ValueError:
        return str(valor)


def formatear_hora(valor):
    """Normaliza a 'HH:MM'. Acepta 'HH:MM:SS' y duraciones ISO ('PT9H30M')."""
    if not valor:
        return ""
    texto = str(valor)
    if texto.startswith("PT"):  # duración ISO devuelta por MySQL para TIME
        horas = re.search(r"(\d+)H", texto)
        minutos = re.search(r"(\d+)M", texto)
        h = int(horas.group(1)) if horas else 0
        m = int(minutos.group(1)) if minutos else 0
        return f"{h:02d}:{m:02d}"
    return texto[:5]  # 'HH:MM:SS' -> 'HH:MM'


# ------------------------------------------------------------------
# Componentes
# ------------------------------------------------------------------
def titulo_seccion(parent, titulo, subtitulo):
    ctk.CTkLabel(
        parent, text=titulo,
        font=ctk.CTkFont(family=FONT_FAMILY, size=22, weight="bold"), text_color=TEXT,
    ).pack(anchor="w")
    ctk.CTkLabel(
        parent, text=subtitulo,
        font=ctk.CTkFont(family=FONT_FAMILY, size=13), text_color=MUTED,
    ).pack(anchor="w", pady=(2, 16))


def tarjeta(parent, titulo=None):
    frame = ctk.CTkFrame(parent, fg_color=CARD, corner_radius=14, border_width=1, border_color=BORDER)
    if titulo:
        ctk.CTkLabel(
            frame, text=titulo,
            font=ctk.CTkFont(family=FONT_FAMILY, size=16, weight="bold"), text_color=TEXT,
        ).pack(anchor="w", padx=18, pady=(16, 6))
        ctk.CTkFrame(frame, height=1, fg_color=BORDER).pack(fill="x", padx=18, pady=(0, 6))
    return frame


def entrada(parent, etiqueta, placeholder, tipo="libre"):
    contenedor = ctk.CTkFrame(parent, fg_color="transparent")
    ctk.CTkLabel(
        contenedor, text=etiqueta.upper(),
        font=ctk.CTkFont(family=FONT_FAMILY, size=11, weight="bold"), text_color=MUTED,
    ).pack(anchor="w", pady=(0, 4))
    campo = ctk.CTkEntry(
        contenedor, placeholder_text=placeholder, height=36, corner_radius=8,
        fg_color=CARD, border_color=BORDER,
        font=ctk.CTkFont(family=FONT_FAMILY, size=12),
    )
    campo.pack(fill="x")

    validador = _crear_validador(campo, tipo)
    if validador is not None:
        campo._entry.configure(validate="key", validatecommand=(validador, "%P"))

    contenedor.entry = campo
    return contenedor


def crear_tabla(parent, columnas, filas, alto=8, ids=None):
    estilo = ttk.Style()
    estilo.theme_use("default")
    estilo.configure(
        "Treeview", background=CARD, foreground=TEXT, rowheight=36,
        fieldbackground=CARD, borderwidth=0, font=(FONT_FAMILY, 10),
    )
    estilo.configure(
        "Treeview.Heading", background=CARD, foreground=MUTED,
        font=(FONT_FAMILY, 10, "bold"), relief="flat", borderwidth=0,
    )
    estilo.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])
    estilo.map("Treeview", background=[("selected", ACCENT)], foreground=[("selected", "white")])

    tabla = ttk.Treeview(parent, columns=columnas, show="headings", height=alto)
    for columna in columnas:
        tabla.heading(columna, text=columna)
        tabla.column(columna, anchor="w", width=140, stretch=True)
    tabla.tag_configure("par", background=ROW_ALT)
    tabla.tag_configure("impar", background=CARD)
    _llenar(tabla, filas, ids)
    return tabla


def actualizar_tabla(tabla, filas, ids=None):
    for item in tabla.get_children():
        tabla.delete(item)
    _llenar(tabla, filas, ids)


def _llenar(tabla, filas, ids):
    ids = ids or []
    for i, fila in enumerate(filas):
        iid = str(ids[i]) if i < len(ids) else None
        tabla.insert("", "end", iid=iid, values=fila, tags=("par" if i % 2 == 0 else "impar",))
