import customtkinter as ctk

# Colores generales del prototipo — paleta sobria de tono profesional
BG = "#F3F4F8"
CARD = "#FFFFFF"
ROW_ALT = "#F8FAFC"
PRIMARY = "#24325F"
PRIMARY_HOVER = "#1B2547"
ACCENT = "#3B5BDB"
ACCENT_HOVER = "#2F4BC0"
SIDEBAR = "#151B2E"
SIDEBAR_HOVER = "#232B45"
TEXT = "#111827"
MUTED = "#6B7280"
BORDER = "#E5E7EB"
SUCCESS = "#15803D"
WARNING = "#B45309"
DANGER = "#B91C1C"
INFO = "#2563EB"

FONT_FAMILY = "Segoe UI"


def configurar_tema():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
