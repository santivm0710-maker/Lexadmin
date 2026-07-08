# Backend - LexAdmin

Esta carpeta contiene la implementación del backend de **LexAdmin**, desarrollada con **FastAPI**. El proyecto mantiene una arquitectura por capas (entidades, repositorios, servicios y rutas) y actualmente cuenta con una **conexión real a una base de datos MySQL**, dejando preparada la estructura para implementar la persistencia completa de la información.

## Objetivo

Representar la capa del servidor de LexAdmin, incluyendo:

* Configuración general del backend.
* Conexión a base de datos MySQL.
* Entidades principales del sistema.
* Repositorios organizados por módulo.
* Servicios para la lógica de negocio.
* Rutas API para cada módulo.
* Separación de responsabilidades para facilitar el mantenimiento y la escalabilidad.

---

# Estructura

```text
backend/
├── main.py
├── config.py
├── requirements.txt
├── README.md
├── database/
│   ├── __init__.py
│   ├── connection.py
│   └── lexadmin.sql
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

---

# Arquitectura

El backend sigue una arquitectura por capas:

```text
Cliente
    │
    ▼
Routes (FastAPI)
    │
    ▼
Services
    │
    ▼
Repositories
    │
    ▼
Database (MySQL)
```

Cada capa tiene una responsabilidad específica:

* **Routes:** reciben las peticiones HTTP.
* **Services:** contienen la lógica de negocio.
* **Repositories:** administran el acceso a los datos.
* **Database:** gestiona la conexión con MySQL.

---

# Base de datos

El proyecto utiliza **MySQL** como gestor de base de datos.

La estructura de la base de datos se encuentra en:

```text
backend/database/lexadmin.sql
```

Este script crea la base de datos **lexadmin** junto con las tablas principales del sistema.

Las tablas implementadas son:

* clientes
* casos
* agenda
* expedientes
* bitacora

Estas tablas representan las entidades utilizadas actualmente por el prototipo.

---

# Conexión a la base de datos

La conexión se encuentra implementada en:

```text
backend/database/connection.py
```

La clase `DatabaseConnection` administra un pool de conexiones mediante `mysql-connector-python`, permitiendo reutilizar conexiones y facilitando futuras operaciones CRUD.

La configuración se obtiene desde `config.py`, donde se definen:

* Host
* Puerto
* Nombre de la base de datos
* Usuario
* Contraseña

---

# Entidades

El backend incluye las entidades principales del sistema:

* Cliente
* Caso
* Expediente
* Agenda
* Información judicial
* Bitácora

Actualmente se utilizan como representación de la información manejada por el sistema y servirán como base para la futura implementación de persistencia completa.

---

# Endpoints disponibles

El backend expone los siguientes endpoints:

```text
GET /
GET /conexion
GET /clientes/
GET /casos/
GET /expedientes/
GET /agenda/
GET /judicial/
GET /bitacora/
GET /dashboard/
GET /reportes/
```

En la versión actual los repositorios continúan utilizando datos simulados, aunque la infraestructura de conexión a MySQL ya se encuentra implementada.

---

# Instalación

Desde la carpeta del backend:

```bash
python -m venv venv
```

Activar el entorno virtual.

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Instalar el conector de MySQL:

```bash
pip install mysql-connector-python
```

---

# Configuración

Modificar los parámetros de conexión en `config.py`:

* database_host
* database_port
* database_name
* database_user
* database_password

También es posible utilizar un archivo `.env` para definir estas variables.

---

# Crear la base de datos

Antes de ejecutar el proyecto, importar el archivo:

```text
backend/database/lexadmin.sql
```

en MySQL Workbench o ejecutar su contenido desde la consola de MySQL.

---

# Ejecutar el backend

Desde la raíz del proyecto:

```bash
uvicorn backend.main:app --reload
```

La documentación automática estará disponible en:

```text
http://127.0.0.1:8000/docs
```

---

# Ejecutar el frontend

En otra terminal:

```bash
cd frontend
python main.py
```

El archivo `frontend/api_client.py` actúa como intermediario entre la interfaz gráfica y la API.

---

# Estado actual

Actualmente el proyecto incluye:

* Arquitectura organizada por capas.
* API desarrollada con FastAPI.
* Conexión real a MySQL.
* Pool de conexiones.
* Script SQL para crear la base de datos.
* Entidades principales.
* Servicios.
* Repositorios.
* Rutas API.
* Configuración centralizada.

Actualmente no incluye:

* CRUD conectado a MySQL.
* Persistencia de información.
* SQLAlchemy.
* Migraciones.
* Autenticación.
* Gestión de usuarios y roles.
* Validaciones completas.
* Carga real de documentos PDF.
* OCR.
* Reportes dinámicos.

---

# Próximas mejoras

Las siguientes funcionalidades podrán incorporarse en futuras versiones:

1. Implementar CRUD utilizando MySQL.
2. Sustituir los datos simulados por consultas reales.
3. Integrar SQLAlchemy como ORM.
4. Implementar migraciones con Alembic.
5. Incorporar autenticación y autorización.
6. Gestionar carga de documentos PDF.
7. Implementar OCR para expedientes.
8. Generar reportes automáticos.
9. Integrar completamente el frontend con la base de datos.
