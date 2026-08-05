# LexAdmin

LexAdmin es un sistema de escritorio para llevar la administración de un
despacho legal: clientes, casos, expedientes, agenda, información judicial,
reportes y una bitácora de auditoría.

Ya no es solo un prototipo visual: está conectado a una base de datos MySQL
de verdad, así que todo lo que se registra desde la aplicación se guarda,
se puede editar y se puede borrar.

```text
backend/    API con FastAPI, conectada a MySQL
frontend/   Interfaz de escritorio hecha con Python y CustomTkinter
```

## Índice

- [Arquitectura](#arquitectura)
- [Lo que necesitas instalado](#lo-que-necesitas-instalado)
- [Instalación](#instalación)
- [Cómo levantar el proyecto](#cómo-levantar-el-proyecto)
- [Trabajar en VS Code](#trabajar-en-vs-code)
- [Cómo se usa](#cómo-se-usa)
- [Endpoints de la API](#endpoints-de-la-api)
- [Qué se hizo sobre el prototipo original](#qué-se-hizo-sobre-el-prototipo-original)
- [Problemas comunes](#problemas-comunes)

## Arquitectura

```text
Lexadmin/
├─ backend/
│  ├─ main.py                # arranca la API (FastAPI)
│  ├─ config.py               # datos de conexión a MySQL
│  ├─ database/
│  │  ├─ connection.py        # pool de conexiones + helpers de consulta
│  │  └─ lexadmin.sql         # crea la base de datos y las tablas
│  ├─ entities/                # cómo luce cada tabla (dataclasses)
│  ├─ repositories/            # el SELECT/INSERT/UPDATE/DELETE de cada tabla
├── services/                # lógica de negocio 
│  ├─ schemas/                 # validación de lo que llega por la API
│  └─ routes/                  # los endpoints
└─ frontend/
   ├─ main.py                 # arranca la ventana
   ├─ app.py                  # ventana principal, menú y navegación
   ├─ api_client.py            # habla con el backend por HTTP
   ├─ crud_frame.py            # base que reutilizan los módulos con formulario
   ├─ styles.py                # colores y tipografía
   ├─ ui_helpers.py            # tablas, campos, combos, validaciones
   └─ frames/                  # una pantalla por módulo
```

En corto: el frontend le pide datos al backend por HTTP, el backend valida y
consulta MySQL, y el resultado vuelve a pintarse en la ventana.

## Lo que necesitas instalado

- **Python 3.12**
- **MySQL o MariaDB** — nosotros usamos el que trae **XAMPP**, así que las
  instrucciones asumen eso (usuario `root`, sin contraseña, que es como viene
  por defecto).
- **Git**
- **Visual Studio Code** (o el editor que prefieras)

## Instalación

**1. Clona el repo**

```bash
git clone https://github.com/santivm0710-maker/Lexadmin.git
cd Lexadmin
```

**2. Crea el entorno virtual e instala las dependencias**

```bash
python -m venv venv

# Windows PowerShell
venv\Scripts\Activate.ps1
# Windows Git Bash
source venv/Scripts/activate

pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

**3. Crea la base de datos**

Con MySQL corriendo (en XAMPP: botón *Start* en la fila de MySQL), corre el
script que crea la base y las tablas:

```bash
"C:\xampp\mysql\bin\mysql.exe" -u root < backend/database/lexadmin.sql

# o, si tienes mysql en el PATH:
mysql -u root < backend/database/lexadmin.sql
```

Ese script crea la base `lexadmin` con las tablas `clientes`, `casos`,
`informacion_judicial`, `expedientes`, `agenda` y `bitacora`. Si lo vuelves a
correr, borra y recrea todo, así que sirve también para dejar la base limpia.

**4. Revisa la conexión**

Si tu MySQL tiene otro usuario o contraseña, cámbialo en `backend/config.py`:

```python
database_host = "localhost"
database_port = 3306
database_name = "lexadmin"
database_user = "root"
database_password = ""     # tu contraseña, si tienes una
```

**5. Configura la clave del JWT**

El backend firma las sesiones con una clave secreta. Para desarrollo hay una
por defecto, pero es buena práctica definir la tuya en un archivo `.env` en
la raíz del proyecto (junto a `backend/` y `frontend/`):

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copia lo que imprima ese comando a un archivo `.env`: JWT_SECRET_KEY="lo que imprima el comando de arriba"

Este archivo nunca se sube al repositorio así que cada quien clone el proyecto debe de crear el suyo.

## Cómo levantar el proyecto

Hay que tener tres cosas prendidas: MySQL, el backend y el frontend.

**MySQL** — ábrelo desde XAMPP y dale *Start* a MySQL.

**Backend** — desde la raíz del proyecto, con el entorno virtual activado:

```bash
uvicorn backend.main:app --reload
```

Queda en `http://127.0.0.1:8000`. La documentación interactiva de la API
está en `http://127.0.0.1:8000/docs`.

**Frontend** — en otra terminal, también con el entorno activado:

```bash
cd frontend
python main.py
```

Si el backend no está corriendo, la ventana igual abre, pero las tablas
salen vacías y al guardar algo va a avisar que no se pudo conectar.

## Trabajar en VS Code

1. Abre la carpeta con `code .`
2. Selecciona el intérprete del entorno virtual: `Ctrl+Shift+P` →
   *Python: Select Interpreter* → `./venv/Scripts/python.exe`.
3. Abre dos terminales integradas: una para el backend
   (`uvicorn backend.main:app --reload`) y otra para el frontend
   (`cd frontend` y luego `python main.py`).
4. Si no la tienes, instala la extensión de Python de Microsoft, ayuda con
   el autocompletado.

## Cómo se usa

- El **menú lateral** cambia de módulo (Inicio, Clientes, Casos...).
- El **buscador** de arriba filtra en vivo la tabla que estés viendo.
- Llenas el formulario y le das a **Guardar / Crear**.
- Para **editar**: seleccionas una fila (o le haces doble clic) y presionas
  *Editar*; el formulario se llena solo y el botón cambia a *Actualizar*.
- Para **eliminar**: seleccionas la fila y presionas *Eliminar*, pide
  confirmación antes de borrar.

Para que todo enlace bien conviene cargar los datos en este orden:
primero **Clientes**, luego **Casos** (ahí eliges el cliente de un
desplegable), y después **Expedientes**, **Agenda** e **Información
judicial** (ahí eliges el caso, también de un desplegable).

Los campos con opciones fijas (estado, prioridad, tipo de proceso, tipo de
documento...) y los que apuntan a otro registro (cliente, caso) se eligen de
una lista en vez de escribirse, para evitar errores de digitación.

Los campos numéricos (identificación, teléfono, fecha, hora) no dejan
escribir letras, y los de puro texto (nombre, juez, fiscal) no dejan
escribir números.

Cada vez que creas, editas o borras algo, queda anotado solo en la
**Bitácora** — no hay que escribir nada ahí a mano. El **Dashboard** y los
**Reportes** también se calculan al momento con lo que haya en la base.

## Endpoints de la API

| Método | Ruta | Qué hace |
|---|---|---|
| GET / POST | `/clientes/` | listar / crear clientes |
| PUT / DELETE | `/clientes/{id}` | editar / eliminar un cliente |
| GET / POST | `/casos/` | listar / crear casos |
| PUT / DELETE | `/casos/{id}` | editar / eliminar un caso |
| GET / POST | `/expedientes/` | listar / crear expedientes |
| PUT / DELETE | `/expedientes/{id}` | editar / eliminar un expediente |
| GET / POST | `/agenda/` | listar / crear eventos |
| PUT / DELETE | `/agenda/{id}` | editar / eliminar un evento |
| GET / POST | `/judicial/` | listar / crear información judicial |
| PUT / DELETE | `/judicial/{id}` | editar / eliminar información judicial |
| GET | `/bitacora/` | historial de auditoría (solo lectura) |
| GET | `/dashboard/` | indicadores del panel principal |
| GET | `/reportes/` | indicadores y resumen |
| GET | `/conexion` | prueba que la API se conecte a MySQL |

Las rutas marcadas con sesión piden un header `Authorization: Bearer <token>`,
que el frontend maneja solo. Para probarlas manualmente desde `/docs`, hay
que iniciar sesión ahí primero y usar el botón **Authorize**.

## Qué se hizo sobre el prototipo original

El proyecto arrancó como un prototipo que mostraba datos de ejemplo fijos
en el código, sin guardar nada de verdad. A partir de ahí se avanzó en
varios frentes:

**Base de datos.** Se tomó el script original (`backend/database/lexadmin.sql`)
como punto de partida y se completó: se agregó la tabla `informacion_judicial`,
los campos de prioridad y abogado responsable en `casos`, y las llaves
foráneas que faltaban entre tablas.

**Backend.** Los repositorios ahora leen y escriben en MySQL en vez de
devolver listas fijas. Se completó el CRUD (crear, listar, editar y
eliminar) en los cinco módulos con formulario. Se agregó una bitácora que
se llena sola con cada acción, y el dashboard y los reportes ahora calculan
sus números en vivo desde la base. También se mejoró el manejo de errores:
antes un dato duplicado o un borrado con dependencias tiraba un error 500
feo, ahora devuelve un mensaje entendible.

**Frontend.** Los formularios quedaron conectados al backend, con
validación de campos (que no se puedan meter letras donde va un número, y
viceversa) y con menús desplegables para las opciones fijas y para elegir
cliente o caso, en vez de tener que escribirlos a mano. Se conectaron
botones que antes no hacían nada (nuevo caso, buscador, cerrar sesión,
editar/eliminar por fila). Y se le dio una vuelta al diseño para que se
viera más sobrio y acorde a un despacho de abogados.

**Autenticación.** El login ahora emite un token JWT en vez de solo devolver
los datos del usuario. Ese token se exige en el resto de la API (todo menos
registro, login y la verificación de conexión), así que ya no se puede leer
ni modificar información sin haber iniciado sesión antes. El frontend lo
maneja de forma transparente: lo guarda al entrar y lo adjunta en cada
petición sin que cada pantalla tenga que preocuparse por eso.

## Problemas comunes

**`Can't connect to MySQL server`** — MySQL está apagado, enciéndelo desde
XAMPP.

**`No se pudo conectar con el backend`** — el backend no está corriendo,
ejecuta `uvicorn backend.main:app --reload`.

**`Access denied for user 'root'`** — tu MySQL tiene otra contraseña,
ajústala en `backend/config.py`.

**La ventana abre pero todo sale vacío** — revisa que el backend esté
corriendo y que la base de datos se haya creado (pasos de instalación 3 y
"Cómo levantar el proyecto").

**`ModuleNotFoundError`** — te faltó activar el entorno virtual o instalar
los `requirements.txt`.

**`No autenticado` / `La sesión expiró`** — el token venció (dura 8 horas) o
el backend se reinició con una clave JWT distinta. Cierra sesión y vuelve a
iniciar sesión.

**`Not Found` al iniciar sesión desde la app** — revisa que
`API_BASE_URL` en `frontend/api_client.py` sea exactamente
`http://127.0.0.1:8000`, sin una `/` al final.

---

Proyecto de la clase, gestión de despacho legal.
