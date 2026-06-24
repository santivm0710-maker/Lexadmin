# LexAdmin

LexAdmin es un prototipo de sistema para la gestión administrativa de un despacho legal.

El proyecto está dividido en dos partes:

```text
frontend/   Interfaz gráfica de escritorio con Python y CustomTkinter.
backend/    Prototipo de API y estructura del servidor sin conexión real a base de datos.
```

## Estado del proyecto

Este proyecto es un prototipo académico.

Incluye una interfaz visual funcional y una estructura inicial de backend, pero todavía no almacena datos de forma persistente ni está conectado a una base de datos real.

## Frontend

El frontend permite visualizar los módulos principales del sistema:

- Dashboard
- Clientes
- Casos legales
- Expedientes
- Agenda
- Información judicial
- Reportes
- Bitácora

Para más detalles, revisar `frontend/README.md`.

## Backend

El backend incluye:

- Prototipo de conexión a base de datos.
- Entidades del sistema.
- Repositorios simulados.
- Servicios por módulo.
- Rutas API simuladas con FastAPI.

Para más detalles, revisar `backend/README.md`.

---

## Integración frontend-backend prototipo

El proyecto ya incluye una integración básica entre el frontend y el backend.

El backend expone endpoints simulados con FastAPI y el frontend los consume mediante el archivo:

```text
frontend/api_client.py
```

La integración funciona así:

- Si el backend está corriendo en `http://127.0.0.1:8000`, el frontend carga datos desde la API.
- Si el backend no está corriendo, el frontend usa los datos locales de `frontend/data.py` como respaldo.
- Todavía no hay conexión real a base de datos.
- Los formularios siguen siendo visuales; los botones todavía no guardan información real.

### Ejecutar integración completa

Terminal 1, desde la raíz del proyecto:

```bash
uvicorn backend.main:app --reload
```

Terminal 2:

```bash
cd frontend
python main.py
```

### Endpoints principales

```text
GET /clientes/
GET /casos/
GET /expedientes/
GET /agenda/
GET /judicial/
GET /bitacora/
GET /dashboard/
GET /reportes/
GET /conexion
```
