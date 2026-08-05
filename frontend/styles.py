import customtkinter as ctk

# ============================================================
# Paleta LexAdmin — "Autoridad Legal Refinada" (navy + dorado,
# tokens semánticos completos: hover, foco, bordes, estados)
# ============================================================
BG = "#F8FAFC"           # fondo general
CARD = "#FFFFFF"         # tarjetas
ROW_ALT = "#F1F5F9"      # filas alternas de tablas

SIDEBAR = "#0F172A"      # barra lateral (navy casi-negro)
SIDEBAR_HOVER = "#1E293B"
SIDEBAR_TEXT = "#CBD5E1"

PRIMARY = "#1E3A8A"      # azul autoridad — interactivo (foco, selección, enlaces)
PRIMARY_HOVER = "#1B3277"
ACCENT = "#B08A46"       # dorado discreto — solo marca (logo, ítem de nav activo)
ACCENT_HOVER = "#9A7838"
INFO = "#2F5BD0"         # azul para acciones secundarias
INFO_HOVER = "#254BB0"

TEXT = "#0F172A"
MUTED = "#64748B"
BORDER = "#CBD5E1"

SUCCESS = "#1F7A46"
SUCCESS_HOVER = "#186237"
SUCCESS_BG = "#F0FDF4"   # fondo de avisos de éxito
DANGER_BG = "#FEF2F2"    # fondo de avisos de error
WARNING = "#B45309"      # semántico (alertas) — distinto de ACCENT (marca)
DANGER = "#DC2626"
DANGER_HOVER = "#B91C1C"
DISABLED = "#E2E8F0"     # fondo de botones/campos deshabilitados
DISABLED_TEXT = "#94A3B8"

FONT_FAMILY = "Segoe UI"
FONT_SERIF = "Georgia"   # solo para la marca: transmite el tono formal de un despacho legal


def configurar_tema():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
