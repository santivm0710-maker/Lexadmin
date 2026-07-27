# LexAdmin

**LexAdmin** es un sistema de escritorio para la gestión administrativa de un
despacho legal: clientes, casos, expedientes, agenda, información judicial,
reportes y una bitácora de auditoría.

El proyecto está conectado a una **base de datos MySQL real**: todo lo que se
registra desde la aplicación se guarda de verdad y se puede consultar, editar
y eliminar.

```text
backend/    API REST con FastAPI + acceso a MySQL
frontend/   Interfaz de escritorio con Python y CustomTkinter
```

---

## 📑 Tabla de contenido
1. [Arquitectura](#-arquitectura)
2. [Requisitos previos](#-requisitos-previos)
3. [Instalación paso a paso](#-instalación-paso-a-paso)
4. [Cómo iniciar el proyecto](#-cómo-iniciar-el-proyecto)
5. [Abrir y trabajar en Visual Studio Code](#-abrir-y-trabajar-en-visual-studio-code)
6. [Cómo se usa la aplicación](#-cómo-se-usa-la-aplicación)
7. [Endpoints de la API](#-endpoints-de-la-api)
8. [Resumen de cambios realizados](#-resumen-de-cambios-realizados)
9. [Solución de problemas](#-solución-de-problemas)

---

## 🏗 Arquitectura

```text
Lexadmin/
├─ backend/
│  ├─ main.py                # arranque de la API (FastAPI)
│  ├─ config.py              # configuración (host, usuario y clave de MySQL)
│  ├─ database/
│  │  ├─ connection.py       # pool de conexiones y helpers de consulta
│  │  └─ lexadmin.sql        # script que crea la base de datos y las tablas
│  ├─ entities/              # estructura de cada tabla (dataclasses)
│  ├─ repositories/          # acceso a datos (SELECT/INSERT/UPDATE/DELETE)
│  ├─ services/              # lógica de negocio + auditoría automática
│  ├─ schemas/               # validación de lo que entra por la API
│  └─ routes/                # endpoints REST
└─ frontend/
   ├─ main.py                # arranque de la ventana
   ├─ app.py                 # ventana principal (menú, buscador, navegación)
   ├─ api_client.py          # comunicación con el backend
   ├─ crud_frame.py          # base reutilizable de los módulos con formulario
   ├─ styles.py              # paleta y tema visual
   ├─ ui_helpers.py          # componentes (tablas, campos, validaciones)
   └─ frames/                # una pantalla por módulo
```

**Flujo de datos:** el frontend llama al backend por HTTP → el backend valida
y ejecuta la consulta en MySQL → devuelve el resultado → el frontend lo muestra.

---

## ✅ Requisitos previos

| Herramienta | Versión recomendada | Para qué |
|-------------|--------------------|----------|
| **Python**  | 3.12               | Ejecutar backend y frontend |
| **MySQL / MariaDB** | 10.4+ (sirve el de **XAMPP**) | Base de datos |
| **Git**     | cualquiera         | Clonar el repositorio |
| **VS Code** | cualquiera         | Editar y ejecutar el proyecto |

> Este proyecto se probó con el MySQL que trae **XAMPP** en Windows
> (`C:\xampp\mysql`), con el usuario `root` y sin contraseña (valores por
> defecto de XAMPP).

---

## 🚀 Instalación paso a paso

### 1. Obtener el proyecto
```bash
git clone https://github.com/Andres06512/Lexadmin.git
cd Lexadmin
```

### 2. Crear el entorno virtual e instalar dependencias
```bash
python -m venv venv

# Windows (PowerShell)
venv\Scripts\Activate.ps1
# Windows (Git Bash)
source venv/Scripts/activate

pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

### 3. Crear la base de datos en MySQL
Con **MySQL corriendo** (en XAMPP: botón **Start** en la fila *MySQL*),
ejecuta el script que crea la base de datos y todas las tablas:

```bash
# Usando el cliente de XAMPP en Windows
"C:\xampp\mysql\bin\mysql.exe" -u root < backend/database/lexadmin.sql

# O, si tienes 'mysql' en el PATH:
mysql -u root < backend/database/lexadmin.sql
```

> El script crea la base `lexadmin` y las tablas `clientes`, `casos`,
> `informacion_judicial`, `expedientes`, `agenda` y `bitacora`.
> Puedes volver a ejecutarlo para dejar la base **limpia** (borra y recrea las
> tablas).

### 4. Revisar la configuración de conexión
Si tu MySQL usa otro usuario o contraseña, edita `backend/config.py`:

```python
database_host = "localhost"
database_port = 3306
database_name = "lexadmin"
database_user = "root"
database_password = ""     # <-- pon aquí tu contraseña si tienes una
```

---

## ▶ Cómo iniciar el proyecto

Necesitas **tres cosas encendidas**: MySQL, el backend y el frontend.

### 1. MySQL
Abre **XAMPP** → **Start** en la fila *MySQL* (debe quedar en verde).

### 2. Backend (API)
Desde la raíz del proyecto, con el entorno virtual activado:
```bash
uvicorn backend.main:app --reload
```
Quedará disponible en `http://127.0.0.1:8000`.
Documentación interactiva: `http://127.0.0.1:8000/docs`.

### 3. Frontend (ventana de escritorio)
En **otra terminal** (también con el entorno virtual activado):
```bash
cd frontend
python main.py
```

> Si el backend no está corriendo, la ventana abre igual pero mostrará las
> tablas vacías y un aviso al intentar guardar.

---

## 🧩 Abrir y trabajar en Visual Studio Code

1. Abre la carpeta del proyecto:
   ```bash
   code .
   ```
2. **Selecciona el intérprete de Python del entorno virtual:**
   `Ctrl + Shift + P` → *Python: Select Interpreter* → elige
   `./venv/Scripts/python.exe`.
3. Abre **dos terminales integradas** (menú *Terminal → New Terminal*):
   - Terminal 1: `uvicorn backend.main:app --reload`
   - Terminal 2: `cd frontend` y luego `python main.py`
4. (Opcional) Instala la extensión **Python** de Microsoft para autocompletado
   y ejecución con el botón ▶.

---

## 🖱 Cómo se usa la aplicación

- **Menú lateral:** navega entre módulos (Inicio, Clientes, Casos, etc.).
- **Buscador (arriba):** filtra en vivo la tabla de la sección actual.
- **Formularios:** completa los campos y presiona **Guardar / Crear**.
- **Editar:** selecciona una fila de la tabla y presiona **✎ Editar**
  (o doble clic); el formulario se llena y el botón cambia a **Actualizar**.
- **Eliminar:** selecciona una fila y presiona **🗑 Eliminar** (pide confirmación).

**Orden recomendado para cargar datos** (por las relaciones entre tablas):
1. **Clientes** →
2. **Casos** (el cliente se elige de un **menú desplegable**) →
3. **Expedientes / Agenda / Información judicial** (el caso se elige de un
   **menú desplegable** por su número de expediente).

**Menús desplegables:** los campos con opciones fijas (estado, prioridad,
tipo de proceso, tipo de documento, estado OCR, actividad) y los que
referencian a otro registro (cliente, caso) se eligen de una lista, no se
escriben.

**Validación de campos:** los campos numéricos (identificación, teléfono,
fecha, hora) solo aceptan números/símbolos válidos, y los de solo texto
(nombre, juez, fiscal…) no aceptan números.

**Bitácora automática:** cada vez que creas, editas o eliminas algo, queda
registrado solo en la **Bitácora** (no se escribe a mano).

**Dashboard y Reportes:** sus números se calculan en vivo desde la base de
datos.

---

## 🔌 Endpoints de la API

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET/POST | `/clientes/` | Listar / crear clientes |
| PUT/DELETE | `/clientes/{id}` | Editar / eliminar cliente |
| GET/POST | `/casos/` | Listar / crear casos |
| PUT/DELETE | `/casos/{id}` | Editar / eliminar caso |
| GET/POST | `/expedientes/` | Listar / crear expedientes |
| PUT/DELETE | `/expedientes/{id}` | Editar / eliminar expediente |
| GET/POST | `/agenda/` | Listar / crear eventos |
| PUT/DELETE | `/agenda/{id}` | Editar / eliminar evento |
| GET/POST | `/judicial/` | Listar / crear info judicial |
| PUT/DELETE | `/judicial/{id}` | Editar / eliminar info judicial |
| GET | `/bitacora/` | Historial de auditoría (solo lectura) |
| GET | `/dashboard/` | Indicadores del panel principal |
| GET | `/reportes/` | Indicadores y resumen |
| GET | `/conexion` | Verifica la conexión con MySQL |

---

## 📝 Resumen de cambios realizados

Partiendo del prototipo original (que mostraba datos de ejemplo fijos), se
completó el sistema para que funcione con una base de datos real:

**Base de datos**
- Se tomó el script original `backend/database/lexadmin.sql` como base y se
  evolucionó: se añadió la tabla `informacion_judicial`, campos de prioridad y
  abogado responsable en `casos`, y llaves foráneas coherentes entre todas las
  tablas.

**Backend**
- Los repositorios ahora leen y escriben en MySQL (antes usaban listas fijas).
- CRUD completo (crear, listar, **editar** y **eliminar**) en los cinco
  módulos con formulario.
- **Bitácora automática:** cada acción queda registrada sola.
- **Dashboard y Reportes** calculan sus cifras en vivo desde la base de datos.
- Manejo claro de errores: duplicados y borrados con dependencias devuelven un
  mensaje entendible (no un error 500).
- Código simplificado con helpers de consulta y una capa base reutilizable.

**Frontend**
- Formularios conectados al backend con **validación de entrada** (números vs.
  texto).
- Botones que antes no hacían nada ahora funcionan: **Nuevo caso**, **buscador**,
  **cerrar sesión**, y **editar/eliminar** en cada módulo.
- Gran simplificación: los módulos comparten una base común (`crud_frame.py`).
- Diseño más elegante y sobrio (paleta de despacho legal, íconos, tablas
  pulidas), pensado para un abogado.

---

## 🛠 Solución de problemas

| Problema | Causa probable | Solución |
|----------|----------------|----------|
| `Can't connect to MySQL server` | MySQL apagado | Inicia MySQL en XAMPP |
| `No se pudo conectar con el backend` | El backend no está corriendo | Ejecuta `uvicorn backend.main:app --reload` |
| `Access denied for user 'root'` | Contraseña distinta | Ajusta `database_password` en `backend/config.py` |
| La ventana abre vacía | Backend apagado o base sin crear | Verifica pasos 3 y 2 de *Cómo iniciar* |
| `ModuleNotFoundError` | Entorno virtual sin activar | Activa `venv` e instala los `requirements.txt` |

---

*Proyecto académico — Gestión de despacho legal.*
