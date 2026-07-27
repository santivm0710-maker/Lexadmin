# LexAdmin - Frontend de escritorio

Interfaz de escritorio hecha con Python y CustomTkinter. Está conectada al
backend FastAPI y, a través de él, a MySQL: los formularios crean, editan y
eliminan información real, con validación de campos y filtrado en vivo.

Consulta el `README.md` de la raíz para la guía completa de instalación y uso.

## Estructura

```text
frontend/
├── main.py            # punto de entrada
├── app.py              # ventana principal, menú, buscador y navegación
├── api_client.py        # toda la comunicación HTTP con el backend
├── crud_frame.py        # base que reutilizan los módulos con formulario
├── data.py              # opciones del menú lateral
├── styles.py             # colores, fuente y tema visual
├── ui_helpers.py          # tablas, campos de texto, combos y validaciones
└── frames/
    ├── sidebar_frame.py       # menú lateral
    ├── dashboard_frame.py     # panel principal
    ├── clientes_frame.py
    ├── casos_frame.py
    ├── expedientes_frame.py
    ├── agenda_frame.py
    ├── judicial_frame.py
    ├── reportes_frame.py
    └── bitacora_frame.py       # solo lectura, se llena sola
```

## Cómo está armado

Los cinco módulos con formulario (clientes, casos, expedientes, agenda e
información judicial) heredan de `CrudFrame` (en `crud_frame.py`), que se
encarga de la parte repetitiva: construir el formulario, guardar, editar,
eliminar, refrescar la tabla y filtrar. Cada módulo solo describe sus propios
campos y cómo convertir sus datos — así se evita repetir la misma lógica ocho
veces.

`api_client.py` es el único archivo que habla con el backend. Expone
funciones genéricas (`listar`, `crear`, `actualizar`, `eliminar`) más algunos
ayudantes para el dashboard, los reportes y para buscar un cliente o un caso
por nombre/expediente.

## Cómo ejecutarlo

Necesita el backend corriendo (ver el README de la raíz). Desde la carpeta
`frontend`:

```bash
pip install -r requirements.txt
python main.py
```

Si el backend no está corriendo, la ventana abre igual pero las tablas salen
vacías y al intentar guardar algo avisa que no se pudo conectar.
