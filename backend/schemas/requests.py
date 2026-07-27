from datetime import date, datetime, time
from typing import Optional

from pydantic import BaseModel


class ClienteCreate(BaseModel):
    nombre: str
    cedula: str
    telefono: Optional[str] = None
    correo: Optional[str] = None
    caso_relacionado: Optional[str] = None


class CasoCreate(BaseModel):
    numero_expediente: str
    id_cliente: int
    tipo_caso: str
    estado: str
    prioridad: str
    abogado_responsable: Optional[str] = None


class ExpedienteCreate(BaseModel):
    id_caso: int
    nombre_documento: str
    tipo_documento: str
    ruta_archivo: Optional[str] = None
    estado_ocr: str = "Pendiente"


class AgendaCreate(BaseModel):
    id_caso: int
    fecha: date
    hora: time
    actividad: str
    lugar: str
    prioridad: str


class JudicialCreate(BaseModel):
    id_caso: int
    juzgado: str
    juez: Optional[str] = None
    fiscal: Optional[str] = None
    contacto_institucional: Optional[str] = None


class BitacoraCreate(BaseModel):
    fecha_hora: datetime
    actor: str
    modulo: str
    accion: str
    detalle: str
