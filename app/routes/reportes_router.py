"""Rutas para generar y descargar reportes automáticos de elementos eliminados."""

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.crud.miembro_crud import listar_eliminados as miembros_eliminados
from app.crud.proyecto_crud import listar_eliminados as proyectos_eliminados
from app.core.database import get_db
from app.core.reportes import generar_reporte_eliminados
import os

router = APIRouter(prefix="/reportes", tags=["Reportes"])

@router.get("/descargar", summary="Descargar reporte de eliminados", description="Genera y descarga un archivo .txt con la lista de miembros y proyectos eliminados.")
def descargar_reporte_eliminados(db: Session = Depends(get_db)):
    miembros = miembros_eliminados(db)
    proyectos = proyectos_eliminados(db)
    ruta = generar_reporte_eliminados(miembros, proyectos)

    return FileResponse(
        path=ruta,
        filename=ruta.split(os.sep)[-1],
        media_type="text/plain"
    )

