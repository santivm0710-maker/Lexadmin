"""Punto de entrada del backend de LexAdmin.

Ejecutar desde la raíz del proyecto con:
    uvicorn backend.main:app --reload

El backend expone una API REST conectada a una base de datos MySQL real.
"""

import mysql.connector
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.config import settings
from backend.database.connection import DatabaseConnection
from backend.routes import (
    agenda_router,
    bitacora_router,
    casos_router,
    clientes_router,
    dashboard_router,
    expedientes_router,
    judicial_router,
    reportes_router,
)
from backend.schemas.common import ApiResponse

app = FastAPI(title=settings.app_name, version=settings.app_version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Traducción de errores comunes de MySQL a respuestas HTTP claras.
MYSQL_ERROR_RESPONSES = {
    1062: (409, "Ya existe un registro con ese valor único (dato duplicado)."),
    1451: (409, "No se puede eliminar: existen registros relacionados que dependen de este."),
    1452: (400, "El registro relacionado (cliente/caso) no existe."),
}


@app.exception_handler(mysql.connector.Error)
async def mysql_error_handler(request: Request, exc: mysql.connector.Error):
    status_code, detail = MYSQL_ERROR_RESPONSES.get(exc.errno, (500, "Error de base de datos."))
    return JSONResponse(status_code=status_code, content={"detail": detail})


app.include_router(clientes_router)
app.include_router(casos_router)
app.include_router(expedientes_router)
app.include_router(dashboard_router)
app.include_router(reportes_router)
app.include_router(agenda_router)
app.include_router(judicial_router)
app.include_router(bitacora_router)


@app.get("/", response_model=ApiResponse)
def home():
    return ApiResponse(
        success=True,
        message="Backend de LexAdmin activo.",
        data={"estado": "activo", "documentacion": "/docs"},
    )


@app.get("/conexion", response_model=ApiResponse)
def probar_conexion():
    """Verifica que el backend puede conectarse realmente a MySQL."""
    conectado = DatabaseConnection.test_connection()
    return ApiResponse(
        success=conectado,
        message="Conexión con MySQL exitosa." if conectado else "No se pudo conectar a MySQL.",
        data={"conectado": conectado, "base_de_datos": settings.database_name},
    )
