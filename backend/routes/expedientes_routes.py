import os
from tempfile import NamedTemporaryFile
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from backend.schemas.common import ApiResponse
from backend.schemas.requests import ExpedienteCreate
from backend.services.auth_dependency import obtener_usuario_actual
from backend.services.expediente_service import ExpedienteService

router = APIRouter(prefix="/expedientes", tags=["expedientes"], dependencies=[Depends(obtener_usuario_actual)])
service = ExpedienteService()


@router.get("/", response_model=ApiResponse)
def listar_expedientes():
    return ApiResponse(success=True, message="Expedientes obtenidos correctamente.", data=service.listar())


@router.post("/", response_model=ApiResponse)
async def crear_expediente(
    id_cliente: int = Form(...),
    id_caso: int = Form(...),
    nombre_documento: Optional[str] = Form(None),
    tipo_documento: Optional[str] = Form(None),
    estado_ocr: Optional[str] = Form("Pendiente"),
    archivo: Optional[UploadFile] = File(None),
):
    expediente = ExpedienteCreate(
        id_cliente=id_cliente,
        id_caso=id_caso,
        nombre_documento=nombre_documento,
        tipo_documento=tipo_documento,
        estado_ocr=estado_ocr,
    )

    archivo_path = None
    if archivo is not None and getattr(archivo, "filename", None):
        with NamedTemporaryFile("wb", suffix=".pdf", delete=False) as tmp:
            contenido = await archivo.read()
            tmp.write(contenido)
            archivo_path = tmp.name

    try:
        resultado = service.crear(expediente, archivo_pdf=archivo_path)
    finally:
        if archivo_path and os.path.exists(archivo_path):
            os.remove(archivo_path)

    return ApiResponse(success=True, message="Expediente creado correctamente.", data=resultado)


@router.put("/{id_expediente}", response_model=ApiResponse)
async def actualizar_expediente(
    id_expediente: int,
    id_cliente: int = Form(...),
    id_caso: int = Form(...),
    nombre_documento: Optional[str] = Form(None),
    tipo_documento: Optional[str] = Form(None),
    estado_ocr: Optional[str] = Form("Pendiente"),
    archivo: Optional[UploadFile] = File(None),
):
    expediente = ExpedienteCreate(
        id_cliente=id_cliente,
        id_caso=id_caso,
        nombre_documento=nombre_documento,
        tipo_documento=tipo_documento,
        estado_ocr=estado_ocr,
    )

    archivo_path = None
    if archivo is not None and getattr(archivo, "filename", None):
        with NamedTemporaryFile("wb", suffix=".pdf", delete=False) as tmp:
            contenido = await archivo.read()
            tmp.write(contenido)
            archivo_path = tmp.name

    try:
        resultado = service.actualizar(id_expediente, expediente, archivo_pdf=archivo_path)
    finally:
        if archivo_path and os.path.exists(archivo_path):
            os.remove(archivo_path)

    if resultado is None:
        raise HTTPException(status_code=404, detail="Expediente no encontrado.")
    return ApiResponse(success=True, message="Expediente actualizado correctamente.", data=resultado)


@router.delete("/{id_expediente}", response_model=ApiResponse)
def eliminar_expediente(id_expediente: int):
    if not service.eliminar(id_expediente):
        raise HTTPException(status_code=404, detail="Expediente no encontrado.")
    return ApiResponse(success=True, message="Expediente eliminado correctamente.", data=None)
