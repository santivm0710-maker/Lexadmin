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
│   └── auth_dependency.py   # valida el token JWT en las rutas protegidas
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
GET   /                     estado del backend                    (público)
GET   /conexion             prueba la conexión a MySQL             (público)

POST  /usuarios/registro    crear cuenta                           (público)
POST  /usuarios/login       iniciar sesión, devuelve un token JWT  (público)
GET   /usuarios/me          valida el token actual                 (requiere sesión)

GET/POST     /clientes/         PUT/DELETE /clientes/{id}          (requiere sesión)
GET/POST     /casos/            PUT/DELETE /casos/{id}             (requiere sesión)
GET/POST     /expedientes/      PUT/DELETE /expedientes/{id}       (requiere sesión)
GET/POST     /agenda/           PUT/DELETE /agenda/{id}            (requiere sesión)
GET/POST     /judicial/         PUT/DELETE /judicial/{id}          (requiere sesión)

GET   /bitacora/            solo lectura, se llena sola             (requiere sesión)
GET   /dashboard/           indicadores calculados en vivo          (requiere sesión)
GET   /reportes/            indicadores calculados en vivo          (requiere sesión)
```

Las rutas que requieren sesión validan un JWT enviado en el header
`Authorization: Bearer <token>`. El token se obtiene desde `/usuarios/login`
y dura 8 horas (configurable en `backend/config.py` con `jwt_expira_minutos`).

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

Lo que ya tiene:

- Arquitectura por capas completa (entidades, repositorios, servicios, rutas).
- Conexión real a MySQL con pool de conexiones.
- CRUD completo (crear, listar, editar, eliminar) en los cinco módulos con
  formulario.
- Bitácora automática y dashboard/reportes calculados en vivo.
- Manejo de errores de MySQL traducido a respuestas HTTP claras (409, 400...).
- Autenticación por JWT: el login emite un token y el resto de la API lo exige.

Lo que falta / posibles mejoras a futuro:

- Autorización por roles (el campo `rol` existe pero aún no restringe acciones).
- Carga real de archivos PDF y OCR de expedientes.
- Un ORM (SQLAlchemy) y migraciones (Alembic), si el proyecto crece.
