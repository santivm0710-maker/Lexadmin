"""Modelos de entrada (lo que el frontend envía al crear/editar)."""

from datetime import date, time
from typing import Optional

from pydantic import BaseModel


class ClienteCreate(BaseModel):
    nombre_completo: str
    identificacion: str
    telefono: Optional[str] = None
    correo: Optional[str] = None


class CasoCreate(BaseModel):
    id_cliente: int
    numero_expediente: str
    tipo_proceso: Optional[str] = None
    estado: Optional[str] = None
    prioridad: Optional[str] = None
    abogado_responsable: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_inicio: Optional[date] = None


class JudicialCreate(BaseModel):
    id_caso: int
    juzgado: Optional[str] = None
    juez: Optional[str] = None
    fiscal: Optional[str] = None
    contacto_institucional: Optional[str] = None


class ExpedienteCreate(BaseModel):
    id_cliente: int
    id_caso: int
    nombre_documento: Optional[str] = None
    tipo_documento: Optional[str] = None
    ruta_pdf: Optional[str] = None
    estado_ocr: Optional[str] = "Pendiente"


class UsuarioRegistro(BaseModel):
    nombre_completo: str
    correo: str
    password: str


class UsuarioLogin(BaseModel):
    correo: str
    password: str


class AgendaCreate(BaseModel):
    id_caso: int
    fecha: date
    hora: time
    actividad: Optional[str] = None
    lugar: Optional[str] = None
    prioridad: Optional[str] = None
    observaciones: Optional[str] = None
