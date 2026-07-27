import customtkinter as ctk

# ============================================================
# Paleta LexAdmin — sobria y profesional (estilo despacho legal)
# ============================================================
BG = "#EEF1F6"          # fondo general
CARD = "#FFFFFF"         # tarjetas
ROW_ALT = "#F6F8FC"      # filas alternas de tablas

SIDEBAR = "#141C2E"      # barra lateral (azul marino profundo)
SIDEBAR_HOVER = "#222C44"
SIDEBAR_TEXT = "#C7CFE0"

PRIMARY = "#1F2A44"      # azul marino
ACCENT = "#B08A46"       # dorado discreto (detalle elegante)
ACCENT_HOVER = "#9A7838"
INFO = "#2F5BD0"         # azul para acciones secundarias
INFO_HOVER = "#254BB0"

TEXT = "#1A2233"
MUTED = "#6B7488"
BORDER = "#E2E6EE"

SUCCESS = "#1F7A46"
SUCCESS_HOVER = "#186237"
WARNING = "#B45309"
DANGER = "#B23B3B"
DANGER_HOVER = "#963030"

FONT_FAMILY = "Segoe UI"


def configurar_tema():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
