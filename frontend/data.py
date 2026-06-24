# Datos de ejemplo para el prototipo visual.
# Luego pueden sustituirse por datos provenientes del backend o base de datos.

MENU_ITEMS = [
    ("dashboard", "Inicio"),
    ("clientes", "Clientes"),
    ("casos", "Casos legales"),
    ("expedientes", "Expedientes"),
    ("agenda", "Agenda"),
    ("judicial", "Info. judicial"),
    ("reportes", "Reportes"),
    ("bitacora", "Bitácora"),
]

DASHBOARD_STATS = [
    ("Clientes registrados", "128", "+12 este mes", "#2563EB"),
    ("Casos activos", "46", "8 prioridad alta", "#F59E0B"),
    ("Audiencias pendientes", "14", "Próxima: 15/06/2026", "#DC2626"),
    ("PDF digitalizados", "312", "OCR procesado", "#16A34A"),
]

CASOS_ATENCION = [
    ("#245", "Juan Pérez", "Pensión alimentaria", "Urgente", "En revisión"),
    ("#246", "María Soto", "Laboral", "Alta", "Activo"),
    ("#247", "Carlos Mora", "Civil", "Media", "Pendiente"),
]

ACTIVIDAD_RECIENTE = [
    ("13/06/2026", "Sistema", "Base de Datos", "Respaldo automático realizado"),
    ("12/06/2026", "Sistema", "Estadísticas", "Casos activos y urgentes actualizados"),
    ("12/06/2026", "Abogado", "Búsqueda Inteligente", "Consulta: Pensión Juan Pérez"),
    ("11/06/2026", "Abogado", "Agenda", "Audiencia registrada para el 15/06/2026"),
]

CLIENTES = [
    ("Juan Pérez", "1-1111-1111", "8888-1234", "juan@email.com", "#245"),
    ("María Soto", "2-2222-2222", "8777-2020", "maria@email.com", "#246"),
    ("Carlos Mora", "3-3333-3333", "8666-3030", "carlos@email.com", "#247"),
]

CASOS = [
    ("#245", "Juan Pérez", "Pensión alimentaria", "En revisión", "Urgente", "Lic. Montero"),
    ("#246", "María Soto", "Laboral", "Activo", "Alta", "Lic. Vargas"),
    ("#247", "Carlos Mora", "Civil", "Pendiente", "Media", "Lic. Solís"),
]

EXPEDIENTES = [
    ("Juan Pérez", "#245", "expediente_245.pdf", "Expediente", "Procesado", "Cliente/Caso/Documento"),
    ("María Soto", "#246", "contrato_laboral.pdf", "Prueba", "Pendiente", "Cliente/Caso/Documento"),
    ("Carlos Mora", "#247", "resolucion.pdf", "Resolución", "Procesado", "Cliente/Caso/Documento"),
]

AGENDA = [
    ("15/06/2026", "09:00", "#245", "Audiencia", "Juzgado de Familia", "Urgente"),
    ("18/06/2026", "14:30", "#246", "Reunión", "Sala 2", "Activo"),
    ("20/06/2026", "08:00", "#247", "Vencimiento", "Presentar escrito", "Alta"),
]

JUDICIAL = [
    ("#245", "Juzgado de Familia", "Dra. Rojas", "Lic. Arias", "familia@poder-judicial.go.cr"),
    ("#246", "Juzgado Laboral", "Dr. Castro", "Lic. Vega", "laboral@poder-judicial.go.cr"),
    ("#247", "Juzgado Civil", "Dra. Núñez", "Lic. Mora", "civil@poder-judicial.go.cr"),
]

REPORTES = [
    ("Clientes", "128 registros", "Administración de clientes activa"),
    ("Casos", "46 activos", "8 con prioridad alta o urgente"),
    ("Agenda", "14 pendientes", "3 eventos esta semana"),
    ("Expedientes", "312 PDF", "289 procesados por OCR"),
    ("Bitácora", "1,240 eventos", "Trazabilidad activa"),
]

BITACORA = [
    ("10/06/2026", "Abogado", "Autenticación", "Inicio de sesión", "El abogado ingresó correctamente al sistema."),
    ("10/06/2026", "Abogado", "Gestión de Clientes", "Registro de cliente", "Se registró el cliente Juan Pérez."),
    ("10/06/2026", "Abogado", "Gestión de Casos", "Creación de caso", "Se creó el caso #245 relacionado con pensión alimentaria."),
    ("10/06/2026", "Abogado", "Expedientes Digitales", "Subida de PDF", "Se cargó un expediente escaneado del caso #245."),
    ("10/06/2026", "Sistema", "Lectura OCR", "Procesamiento automático", "El sistema analizó automáticamente el contenido del PDF."),
    ("11/06/2026", "Abogado", "Agenda y Audiencias", "Programación de audiencia", "Se registró audiencia para el 15/06/2026."),
    ("11/06/2026", "Sistema", "Recordatorios", "Generación de alerta", "Se creó un recordatorio automático."),
    ("12/06/2026", "Sistema", "Estadísticas", "Generación de reporte", "Se actualizaron estadísticas de casos activos y urgentes."),
    ("13/06/2026", "Sistema", "Base de Datos", "Respaldo automático", "Se realizó una copia de seguridad de la información."),
]
