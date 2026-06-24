from fastapi import APIRouter

from backend.schemas.common import ApiResponse

router = APIRouter(prefix="/reportes", tags=["reportes"])


@router.get("/", response_model=ApiResponse)
def obtener_reportes():
    """Devuelve indicadores simulados para el módulo de reportes."""
    return ApiResponse(
        success=True,
        message="Reportes simulados obtenidos correctamente.",
        data={
            "indicadores": [
                ("Casos activos", "2", "#0EA5E9"),
                ("Casos finalizados", "0", "#16A34A"),
                ("Urgentes", "1", "#DC2626"),
                ("Audiencias", "2", "#F59E0B"),
                ("PDF OCR", "1", "#16A34A"),
                ("Eventos bitácora", "2", "#2563EB"),
            ],
            "resumen": [
                ("Clientes", "2 registros", "Datos servidos desde endpoint /clientes."),
                ("Casos", "2 registrados", "Datos servidos desde endpoint /casos."),
                ("Agenda", "2 eventos", "Datos servidos desde endpoint /agenda."),
                ("Expedientes", "2 documentos", "Datos servidos desde endpoint /expedientes."),
                ("Bitácora", "2 eventos", "Datos servidos desde endpoint /bitacora."),
            ],
        },
    )
