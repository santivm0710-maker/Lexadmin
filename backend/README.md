# Backend - LexAdmin

Esta carpeta contiene el backend de **LexAdmin**, hecho con **FastAPI**. Sigue
una arquitectura por capas (entidades, repositorios, servicios y rutas) y está
conectado a una base de datos **MySQL real**: ya no hay datos simulados, todo
lo que expone la API sale de la base de datos.

Para la guía completa de instalación y uso, revisa el `README.md` de la raíz
del proyecto. Este archivo se enfoca en explicar cómo está armado el backend.

## Estructura

```text
backend/
├── main.py
├── config.py
├── requirements.txt
├── test_connection.py
├── database/
│   ├── connection.py       # pool de conexiones + helpers de consulta
│   └── lexadmin.sql        # crea la base de datos y las tablas
├── entities/                # una clase por tabla (cliente, caso, expediente...)
├── repositories/            # SELECT/INSERT/UPDATE/DELETE de cada tabla
├── services/                # lógica de negocio + registro automático en bitácora
├── schemas/                 # validación de lo que llega por la API (pydantic)
└── routes/                  # los endpoints de FastAPI
```

## Arquitectura

```text
Cliente (frontend)
    │
    ▼
Routes (FastAPI)     recibe la petición HTTP y valida el body
    │
    ▼
Services              lógica de negocio, y registra la acción en la bitácora
    │
    ▼
Repositories          arma y ejecuta el SQL
    │
    ▼
Database (MySQL)
```

## Base de datos

El script `backend/database/lexadmin.sql` crea la base `lexadmin` con las
tablas `clientes`, `casos`, `informacion_judicial`, `expedientes`, `agenda`
y `bitacora`, con sus llaves foráneas correspondientes.

## Conexión a la base de datos

`backend/database/connection.py` mantiene un pool de conexiones
(`mysql-connector-python`) y expone unos helpers (`fetch_all`, `fetch_one`,
`execute`) que usan los repositorios para no repetir el manejo de cursores en
cada consulta. Los datos de conexión (host, puerto, usuario, contraseña) se
configuran en `config.py`.

## Endpoints disponibles

```text
GET   /                     estado del backend
GET   /conexion             prueba la conexión a MySQL

GET/POST     /clientes/         PUT/DELETE /clientes/{id}
GET/POST     /casos/            PUT/DELETE /casos/{id}
GET/POST     /expedientes/      PUT/DELETE /expedientes/{id}
GET/POST     /agenda/           PUT/DELETE /agenda/{id}
GET/POST     /judicial/         PUT/DELETE /judicial/{id}

GET   /bitacora/            solo lectura, se llena sola
GET   /dashboard/           indicadores calculados en vivo
GET   /reportes/            indicadores calculados en vivo
```

Todos están documentados automáticamente en `/docs` una vez que el backend
está corriendo.

## Instalación rápida

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/macOS

pip install -r requirements.txt
```

Antes de correrlo, crea la base de datos con el script de `database/lexadmin.sql`
(los pasos completos están en el README de la raíz).

## Ejecutarlo

Desde la raíz del proyecto (no desde esta carpeta):

```bash
uvicorn backend.main:app --reload
```

Documentación interactiva en `http://127.0.0.1:8000/docs`.

## Estado actual

Lo que ya tiene:

- Arquitectura por capas completa (entidades, repositorios, servicios, rutas).
- Conexión real a MySQL con pool de conexiones.
- CRUD completo (crear, listar, editar, eliminar) en los cinco módulos con
  formulario.
- Bitácora automática y dashboard/reportes calculados en vivo.
- Manejo de errores de MySQL traducido a respuestas HTTP claras (409, 400...).

Lo que falta / posibles mejoras a futuro:

- Autenticación y manejo de usuarios/roles.
- Carga real de archivos PDF y OCR de expedientes.
- Un ORM (SQLAlchemy) y migraciones (Alembic), si el proyecto crece.
