"""Reportes e indicadores calculados en vivo desde la base de datos."""

from backend.database.connection import DatabaseConnection


def _contar(sql, params=None):
    fila = DatabaseConnection.fetch_one(sql, params)
    return list(fila.values())[0] if fila else 0


class ReportesService:
    def resumen(self):
        clientes = _contar("SELECT COUNT(*) FROM clientes")
        casos = _contar("SELECT COUNT(*) FROM casos")
        cerrados = _contar("SELECT COUNT(*) FROM casos WHERE estado IN ('Cerrado', 'Finalizado')")
        urgentes = _contar("SELECT COUNT(*) FROM casos WHERE prioridad IN ('Alta', 'Urgente')")
        audiencias = _contar("SELECT COUNT(*) FROM agenda")
        expedientes = _contar("SELECT COUNT(*) FROM expedientes")
        eventos = _contar("SELECT COUNT(*) FROM bitacora")

        indicadores = [
            ("Casos totales", str(casos), "#2563EB"),
            ("Casos cerrados", str(cerrados), "#15803D"),
            ("Prioridad alta", str(urgentes), "#B91C1C"),
            ("Audiencias", str(audiencias), "#B45309"),
            ("Expedientes", str(expedientes), "#15803D"),
            ("Eventos bitácora", str(eventos), "#24325F"),
        ]

        resumen = [
            ("Clientes", f"{clientes} registros", "Cartera de clientes del despacho."),
            ("Casos", f"{casos} en total", f"{urgentes} con prioridad alta o urgente."),
            ("Agenda", f"{audiencias} eventos", "Audiencias y actividades programadas."),
            ("Expedientes", f"{expedientes} documentos", "Archivos digitalizados por caso."),
            ("Bitácora", f"{eventos} eventos", "Trazabilidad de acciones del sistema."),
        ]

        return {"indicadores": indicadores, "resumen": resumen}
