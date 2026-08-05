"""Iconografía monocroma de LexAdmin.

Usa la fuente de sistema Segoe MDL2 Assets (viene instalada con Windows,
sin dependencias externas de íconos) en vez de emojis, para que cada ícono
herede el color de la paleta en lugar de mostrarse a todo color.

CustomTkinter no permite mezclar dos fuentes dentro de un mismo texto de
botón, así que los glifos se renderizan una sola vez como bitmaps (vía
Pillow) y se cachean como CTkImage para usarlos con `image=` en
CTkButton/CTkLabel.
"""

from functools import lru_cache

import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont

ICON_FONT_PATH = r"C:\Windows\Fonts\segmdl2.ttf"

GLIFOS = {
    "dashboard": "\uE80A",
    "clientes": "\uE77B",
    "casos": "\uE821",
    "expedientes": "\uE838",
    "agenda": "\uE787",
    "judicial": "\uE825",
    "reportes": "\uE9F9",
    "bitacora": "\uE823",
    "buscar": "\uE721",
    "eliminar": "\uE74D",
    "editar": "\uE70F",
    "agregar": "\uE710",
    "check": "\uE73E",
    "salir": "\uE7E8",
    "ver": "\uE7B3",
    "ocultar": "\uED1A",
    "correo": "\uE715",
    "escudo": "\uEA18",
}


@lru_cache(maxsize=None)
def _fuente(tamano_muestreo):
    return ImageFont.truetype(ICON_FONT_PATH, tamano_muestreo)


@lru_cache(maxsize=None)
def imagen(nombre, tamano=16, color="#1A2233"):
    """Renderiza un glifo como CTkImage monocromo, centrado y suavizado."""
    glifo = GLIFOS.get(nombre, nombre)
    escala = 4
    lienzo = tamano * escala
    img = Image.new("RGBA", (lienzo, lienzo), (0, 0, 0, 0))
    dibujo = ImageDraw.Draw(img)
    fuente = _fuente(int(lienzo * 0.75))
    caja = dibujo.textbbox((0, 0), glifo, font=fuente)
    ancho, alto = caja[2] - caja[0], caja[3] - caja[1]
    pos = ((lienzo - ancho) / 2 - caja[0], (lienzo - alto) / 2 - caja[1])
    dibujo.text(pos, glifo, font=fuente, fill=color)
    img = img.resize((tamano, tamano), Image.LANCZOS)
    return ctk.CTkImage(light_image=img, size=(tamano, tamano))
