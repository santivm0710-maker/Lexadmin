"""Indicadores del dashboard calculados en vivo desde la base de datos."""

from backend.database.connection import DatabaseConnection


def _contar(sql, params=None):
    fila = DatabaseConnection.fetch_one(sql, params)
    return list(fila.values())[0] if fila else 0


class DashboardService:
    def resumen(self):
        total_clientes = _contar("SELECT COUNT(*) FROM clientes")
        total_casos = _contar("SELECT COUNT(*) FROM casos")
        urgentes = _contar(
            "SELECT COUNT(*) FROM casos WHERE prioridad IN ('Alta', 'Urgente')"
        )
        audiencias = _contar("SELECT COUNT(*) FROM agenda WHERE fecha >= CURDATE()")
        expedientes = _contar("SELECT COUNT(*) FROM expedientes")

        stats = [
            ("Clientes registrados", str(total_clientes), "Total en el sistema", "#2563EB"),
            ("Casos activos", str(total_casos), f"{urgentes} de prioridad alta", "#B45309"),
            ("Audiencias próximas", str(audiencias), "A partir de hoy", "#B91C1C"),
            ("Expedientes", str(expedientes), "Documentos digitalizados", "#15803D"),
        ]

        casos_atencion = [
            (
                fila["numero_expediente"],
                fila["nombre_completo"],
                fila["tipo_proceso"] or "-",
                fila["prioridad"] or "-",
                fila["estado"] or "-",
            )
            for fila in DatabaseConnection.fetch_all(
                """
                SELECT c.numero_expediente, c.tipo_proceso, c.prioridad, c.estado,
                       cl.nombre_completo
                FROM casos c
                JOIN clientes cl ON cl.id_cliente = c.id_cliente
                ORDER BY FIELD(c.prioridad, 'Urgente', 'Alta', 'Media', 'Baja'), c.id_caso DESC
                LIMIT 8
                """
            )
        ]

        actividad = [
            (
                _fecha(fila["fecha"]),
                fila["actor"] or "-",
                fila["modulo"] or "-",
                fila["descripcion"] or "",
            )
            for fila in DatabaseConnection.fetch_all(
                "SELECT fecha, actor, modulo, descripcion FROM bitacora "
                "ORDER BY id_bitacora DESC LIMIT 6"
            )
        ]

        return {"stats": stats, "casos_atencion": casos_atencion, "actividad_reciente": actividad}


def _fecha(valor):
    try:
        return valor.strftime("%d/%m/%Y")
    except AttributeError:
        return str(valor or "")
