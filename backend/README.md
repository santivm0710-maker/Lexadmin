# Backend prototipo - LexAdmin

Esta carpeta contiene la estructura inicial del backend para LexAdmin.

El backend está diseñado como un prototipo, por lo que todavía **no se conecta a una base de datos real**. Su objetivo es dejar preparada la organización del código para una futura conexión con una base de datos y para una posible integración con el frontend.

## Objetivo

Representar la capa del servidor de LexAdmin, incluyendo:

- Configuración general del backend.
- Prototipo de conexión a base de datos.
- Entidades principales del sistema.
- Repositorios simulados con datos de ejemplo.
- Servicios por módulo.
- Rutas API simuladas.
- Separación de responsabilidades para facilitar futuras mejoras.

## Estructura

```text
backend/
├── main.py
├── config.py
├── requirements.txt
├── README.md
├── database/
│   ├── __init__.py
│   └── connection.py
├── entities/
│   ├── __init__.py
│   ├── cliente.py
│   ├── caso.py
│   ├── expediente.py
│   ├── agenda.py
│   ├── judicial.py
│   └── bitacora.py
├── repositories/
│   ├── __init__.py
│   ├── base_repository.py
│   ├── mock_data.py
│   ├── cliente_repository.py
│   ├── caso_repository.py
│   ├── expediente_repository.py
│   ├── agenda_repository.py
│   ├── judicial_repository.py
│   └── bitacora_repository.py
├── services/
│   ├── __init__.py
│   ├── cliente_service.py
│   ├── caso_service.py
│   ├── expediente_service.py
│   ├── agenda_service.py
│   ├── judicial_service.py
│   └── bitacora_service.py
├── routes/
│   ├── __init__.py
│   ├── clientes_routes.py
│   ├── casos_routes.py
│   ├── expedientes_routes.py
│   ├── agenda_routes.py
│   ├── judicial_routes.py
│   └── bitacora_routes.py
└── schemas/
    ├── __init__.py
    └── common.py
```

## Entidades incluidas

El backend contiene entidades base para los módulos principales del sistema:

- Cliente
- Caso
- Expediente
- Evento de agenda
- Información judicial
- Evento de bitácora

Estas entidades están creadas con `dataclass` para representar la estructura de datos del sistema antes de implementar modelos definitivos de base de datos.

## Prototipo de conexión

El archivo `database/connection.py` contiene una clase llamada `DatabaseConnectionPrototype`.

Esta clase solo prepara los datos de conexión, pero no realiza una conexión real.

```python
def connect(self):
    raise NotImplementedError("La conexión real a base de datos todavía no está implementada.")
```

Esto permite mostrar que el proyecto está preparado para una conexión futura sin depender todavía de MySQL, PostgreSQL, SQLite u otro motor.

## Rutas simuladas

El backend incluye rutas API para consultar datos de ejemplo:

```text
GET /
GET /conexion
GET /clientes/
GET /casos/
GET /expedientes/
GET /agenda/
GET /judicial/
GET /bitacora/
```

Todas las rutas devuelven información simulada desde listas internas.

## Instalación

Desde la raíz del proyecto:

```bash
cd backend
python -m venv venv
```

Activar el entorno virtual.

En Windows:

```bash
venv\Scripts\activate
```

En macOS o Linux:

```bash
source venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

Desde la raíz del proyecto, ejecutar:

```bash
uvicorn backend.main:app --reload
```

Luego abrir en el navegador:

```text
http://127.0.0.1:8000/docs
```

Ahí se puede visualizar la documentación automática de las rutas del backend.

## Estado actual

Incluye:

- Estructura de backend organizada.
- API prototipo con FastAPI.
- Entidades principales del sistema.
- Repositorios simulados.
- Servicios por módulo.
- Rutas con datos de ejemplo.
- Prototipo de configuración de conexión.

No incluye todavía:

- Conexión real a base de datos.
- Tablas SQL.
- ORM como SQLAlchemy.
- Migraciones.
- Autenticación.
- Validaciones completas.
- Integración real con el frontend.
- Almacenamiento persistente.

## Siguientes pasos sugeridos

Para convertir este prototipo en un backend funcional, se podrían implementar:

1. Base de datos SQLite, PostgreSQL o MySQL.
2. Modelos ORM con SQLAlchemy.
3. Migraciones con Alembic.
4. CRUD completo para cada entidad.
5. Autenticación de usuarios.
6. Roles para abogado, asistente y administrador.
7. Integración con el frontend de CustomTkinter.
8. Carga real de documentos PDF.
9. OCR para lectura de expedientes.
10. Generación de reportes.

---

## Endpoints conectados al frontend

El frontend consume de forma prototipo los siguientes endpoints:

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

Estos endpoints devuelven datos simulados desde memoria. Todavía no existe conexión real a base de datos.

## Probar con el frontend

Desde la raíz del proyecto, ejecutar:

```bash
uvicorn backend.main:app --reload
```

Luego, en otra terminal:

```bash
cd frontend
python main.py
```

El archivo `frontend/api_client.py` es el puente entre la interfaz gráfica y la API prototipo.
