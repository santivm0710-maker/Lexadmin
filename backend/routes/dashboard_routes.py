from fastapi import APIRouter

from backend.schemas.common import ApiResponse

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/", response_model=ApiResponse)
def obtener_dashboard():
    """Devuelve datos simulados para el dashboard del frontend."""
    return ApiResponse(
        success=True,
        message="Dashboard simulado obtenido correctamente.",
        data={
            "stats": [
                ("Clientes registrados", "2", "Datos desde backend", "#2563EB"),
                ("Casos activos", "2", "1 prioridad urgente", "#F59E0B"),
                ("Audiencias pendientes", "2", "Próxima: 15/06/2026", "#DC2626"),
                ("PDF digitalizados", "2", "1 OCR procesado", "#16A34A"),
            ],
            "casos_atencion": [
                ("#245", "Juan Pérez", "Pensión alimentaria", "Urgente", "En revisión"),
                ("#246", "María Rodríguez", "Laboral", "Media", "Activo"),
            ],
            "actividad_reciente": [
                ("10/06/2026", "Sistema", "Clientes", "Se registró cliente de ejemplo desde backend."),
                ("10/06/2026", "Sistema", "Casos", "Se creó caso de ejemplo #245."),
                ("10/06/2026", "Sistema", "Backend", "API prototipo activa sin base de datos."),
            ],
        },
    )
