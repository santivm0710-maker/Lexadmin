"""Punto de entrada del backend prototipo de LexAdmin.

Ejecutar desde la raíz del proyecto con:
    uvicorn backend.main:app --reload

Este backend expone rutas simuladas y no se conecta a una base de datos real.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.database.connection import get_database_prototype
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
        message="Backend prototipo de LexAdmin activo.",
        data={
            "estado": "prototipo",
            "base_de_datos": "no conectada",
            "documentacion": "/docs",
        },
    )


@app.get("/conexion", response_model=ApiResponse)
def conexion_prototipo():
    db = get_database_prototype()
    return ApiResponse(
        success=True,
        message="Prototipo de configuración de conexión cargado. No se abrió conexión real.",
        data={"connection_preview": db.get_connection_string_preview()},
    )
