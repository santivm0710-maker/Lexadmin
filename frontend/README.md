# LexAdmin - Frontend visual en CustomTkinter

Prototipo visual de escritorio para un sistema de gestión de despacho legal.
No contiene funcionalidades reales, conexión a base de datos, backend, OCR ni autenticación funcional.
Está pensado para que después se conecte con controladores, servicios o backend.

## Estructura organizada por clases

```text
frontend/
├── main.py
├── app.py
├── data.py
├── styles.py
├── ui_helpers.py
├── requirements.txt
├── README.md
└── frames/
    ├── __init__.py
    ├── sidebar_frame.py
    ├── dashboard_frame.py
    ├── clientes_frame.py
    ├── casos_frame.py
    ├── expedientes_frame.py
    ├── agenda_frame.py
    ├── judicial_frame.py
    ├── reportes_frame.py
    └── bitacora_frame.py
```

## Qué contiene cada archivo

- `main.py`: punto de entrada del programa.
- `app.py`: ventana principal `LegalDeskApp`, navegación, header y contenedor de páginas.
- `data.py`: datos de ejemplo del prototipo.
- `styles.py`: colores y configuración visual general.
- `ui_helpers.py`: funciones reutilizables para títulos, tarjetas, tablas y entradas.
- `frames/sidebar_frame.py`: clase `SidebarFrame`.
- `frames/dashboard_frame.py`: clase `DashboardFrame`.
- `frames/clientes_frame.py`: clase `ClientesFrame`.
- `frames/casos_frame.py`: clase `CasosFrame`.
- `frames/expedientes_frame.py`: clase `ExpedientesFrame`.
- `frames/agenda_frame.py`: clase `AgendaFrame`.
- `frames/judicial_frame.py`: clase `JudicialFrame`.
- `frames/reportes_frame.py`: clase `ReportesFrame`.
- `frames/bitacora_frame.py`: clase `BitacoraFrame`.

## Cómo ejecutar

Desde la carpeta `frontend`:

```bash
pip install -r requirements.txt
python main.py
```

## Nota

La lógica visual se mantiene igual, pero ahora cada frame está separado en su propio archivo para que sea más fácil mantener, revisar y ampliar el proyecto.

---

## Conexión con el backend prototipo

El frontend incluye el archivo `api_client.py`, que intenta leer datos desde el backend FastAPI en:

```bash
http://127.0.0.1:8000
```

Para probar la integración:

1. Ejecutar primero el backend desde la raíz del proyecto:

```bash
uvicorn backend.main:app --reload
```

2. En otra terminal, ejecutar el frontend:

```bash
cd frontend
python main.py
```

Si el backend está activo, las tablas de clientes, casos, expedientes, agenda, información judicial, reportes, dashboard y bitácora consumirán los endpoints simulados.

Si el backend no está activo, el frontend usará automáticamente los datos locales de `data.py` como respaldo. Esto permite seguir usando el prototipo visual aunque la API no esté corriendo.
