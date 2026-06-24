from datetime import date, datetime, time

from backend.entities import (
    BitacoraEvento,
    Caso,
    Cliente,
    EventoAgenda,
    Expediente,
    InformacionJudicial,
)

CLIENTES = [
    Cliente(1, "Juan Pérez", "1-1111-1111", "8888-0000", "juan@example.com", "Caso #245"),
    Cliente(2, "María Rodríguez", "2-2222-2222", "8999-1111", "maria@example.com", "Caso #246"),
]

CASOS = [
    Caso(1, "#245", 1, "Pensión alimentaria", "En revisión", "Urgente", "Abogado principal"),
    Caso(2, "#246", 2, "Laboral", "Activo", "Media", "Abogado principal"),
]

EXPEDIENTES = [
    Expediente(1, 1, "expediente_245.pdf", "Expediente principal", "/docs/expediente_245.pdf", "Pendiente"),
    Expediente(2, 2, "contrato_laboral.pdf", "Prueba documental", "/docs/contrato_laboral.pdf", "Procesado"),
]

AGENDA = [
    EventoAgenda(1, 1, date(2026, 6, 15), time(9, 0), "Audiencia", "Juzgado de Familia", "Alta"),
    EventoAgenda(2, 2, date(2026, 6, 18), time(14, 30), "Reunión con cliente", "Oficina", "Media"),
]

INFO_JUDICIAL = [
    InformacionJudicial(1, 1, "Juzgado de Familia", "Lic. Ana Mora", None, "familia@example.go.cr"),
    InformacionJudicial(2, 2, "Juzgado Laboral", "Lic. Carlos Rojas", "Fiscalía Laboral", "laboral@example.go.cr"),
]

BITACORA = [
    BitacoraEvento(1, datetime(2026, 6, 10, 8, 30), "Sistema", "Clientes", "Registro", "Se registró cliente de ejemplo."),
    BitacoraEvento(2, datetime(2026, 6, 10, 8, 35), "Sistema", "Casos", "Creación", "Se creó caso de ejemplo #245."),
]
