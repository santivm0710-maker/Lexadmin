import customtkinter as ctk
from tkinter import ttk

from styles import CARD, TEXT, MUTED, BORDER


def titulo_seccion(parent, titulo, subtitulo):
    ctk.CTkLabel(
        parent,
        text=titulo,
        font=ctk.CTkFont(size=22, weight="bold"),
        text_color=TEXT,
    ).pack(anchor="w")
    ctk.CTkLabel(
        parent,
        text=subtitulo,
        font=ctk.CTkFont(size=13),
        text_color=MUTED,
    ).pack(anchor="w", pady=(2, 14))


def tarjeta(parent, titulo=None):
    frame = ctk.CTkFrame(parent, fg_color=CARD, corner_radius=16, border_width=1, border_color=BORDER)
    if titulo:
        ctk.CTkLabel(
            frame,
            text=titulo,
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color=TEXT,
        ).pack(anchor="w", padx=18, pady=(16, 8))
    return frame


def crear_tabla(parent, columnas, filas, alto=8, ids=None):
    style = ttk.Style()
    style.theme_use("default")
    style.configure(
        "Treeview",
        background="white",
        foreground=TEXT,
        rowheight=34,
        fieldbackground="white",
        borderwidth=0,
        font=("Segoe UI", 10),
    )
    style.configure(
        "Treeview.Heading",
        background="#EEF2FF",
        foreground=TEXT,
        font=("Segoe UI", 10, "bold"),
        relief="flat",
    )

    tabla = ttk.Treeview(parent, columns=columnas, show="headings", height=alto)
    for columna in columnas:
        tabla.heading(columna, text=columna)
        tabla.column(columna, anchor="w", width=140, stretch=True)
    ids = ids or []
    for i, fila in enumerate(filas):
        iid = str(ids[i]) if i < len(ids) else None
        tabla.insert("", "end", iid=iid, values=fila)
    return tabla


def entrada(parent, etiqueta, placeholder):
    contenedor = ctk.CTkFrame(parent, fg_color="transparent")
    ctk.CTkLabel(
        contenedor,
        text=etiqueta,
        font=ctk.CTkFont(size=12, weight="bold"),
        text_color=TEXT,
    ).pack(anchor="w", pady=(0, 5))
    campo = ctk.CTkEntry(
        contenedor,
        placeholder_text=placeholder,
        height=38,
        fg_color="white",
        border_color=BORDER,
    )
    campo.pack(fill="x")
    contenedor.entry = campo
    return contenedor


def actualizar_tabla(tabla, filas, ids=None):
    for item in tabla.get_children():
        tabla.delete(item)
    ids = ids or []
    for i, fila in enumerate(filas):
        iid = str(ids[i]) if i < len(ids) else None
        tabla.insert("", "end", iid=iid, values=fila)
