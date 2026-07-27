import customtkinter as ctk
from tkinter import ttk

from styles import ACCENT, BORDER, CARD, FONT_FAMILY, MUTED, ROW_ALT, TEXT


def titulo_seccion(parent, titulo, subtitulo):
    ctk.CTkLabel(
        parent,
        text=titulo,
        font=ctk.CTkFont(family=FONT_FAMILY, size=22, weight="bold"),
        text_color=TEXT,
    ).pack(anchor="w")
    ctk.CTkLabel(
        parent,
        text=subtitulo,
        font=ctk.CTkFont(family=FONT_FAMILY, size=13),
        text_color=MUTED,
    ).pack(anchor="w", pady=(2, 16))


def tarjeta(parent, titulo=None):
    frame = ctk.CTkFrame(parent, fg_color=CARD, corner_radius=14, border_width=1, border_color=BORDER)
    if titulo:
        ctk.CTkLabel(
            frame,
            text=titulo,
            font=ctk.CTkFont(family=FONT_FAMILY, size=16, weight="bold"),
            text_color=TEXT,
        ).pack(anchor="w", padx=18, pady=(16, 10))
    return frame


def crear_tabla(parent, columnas, filas, alto=8, ids=None):
    style = ttk.Style()
    style.theme_use("default")
    style.configure(
        "Treeview",
        background=CARD,
        foreground=TEXT,
        rowheight=36,
        fieldbackground=CARD,
        borderwidth=0,
        font=(FONT_FAMILY, 10),
    )
    style.configure(
        "Treeview.Heading",
        background=CARD,
        foreground=MUTED,
        font=(FONT_FAMILY, 10, "bold"),
        relief="flat",
        borderwidth=0,
    )
    style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])
    style.map(
        "Treeview",
        background=[("selected", ACCENT)],
        foreground=[("selected", "white")],
    )

    tabla = ttk.Treeview(parent, columns=columnas, show="headings", height=alto)
    for columna in columnas:
        tabla.heading(columna, text=columna)
        tabla.column(columna, anchor="w", width=140, stretch=True)
    tabla.tag_configure("par", background=ROW_ALT)
    tabla.tag_configure("impar", background=CARD)

    ids = ids or []
    for i, fila in enumerate(filas):
        iid = str(ids[i]) if i < len(ids) else None
        tabla.insert("", "end", iid=iid, values=fila, tags=("par" if i % 2 == 0 else "impar",))
    return tabla


def entrada(parent, etiqueta, placeholder):
    contenedor = ctk.CTkFrame(parent, fg_color="transparent")
    ctk.CTkLabel(
        contenedor,
        text=etiqueta,
        font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"),
        text_color=TEXT,
    ).pack(anchor="w", pady=(0, 5))
    campo = ctk.CTkEntry(
        contenedor,
        placeholder_text=placeholder,
        height=36,
        corner_radius=8,
        fg_color=CARD,
        border_color=BORDER,
        font=ctk.CTkFont(family=FONT_FAMILY, size=12),
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
        tabla.insert("", "end", iid=iid, values=fila, tags=("par" if i % 2 == 0 else "impar",))
