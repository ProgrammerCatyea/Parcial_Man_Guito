"""Rutas para generar y descargar reportes automáticos de elementos eliminados."""
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.reportes import generar_reporte_txt
from app.crud.proyecto_crud import listar_proyectos, listar_proyectos_eliminados
from app.crud.miembro_crud import listar_miembros_eliminados as miembros_eliminados
import os

router = APIRouter(prefix="/reportes", tags=["Reportes"])

@router.get("/descargar")
def descargar_reporte(db: Session = Depends(get_db)):
   
    proyectos = listar_proyectos(db)
    proyectos_eliminados = listar_proyectos_eliminados(db)
    miembros = miembros_eliminados(db)

    ruta_archivo = generar_reporte_txt(proyectos, proyectos_eliminados, miembros)

    if not os.path.exists(ruta_archivo):
        return {"error": "No se pudo generar el reporte."}

    return FileResponse(
        ruta_archivo,
        media_type="text/plain",
        filename="reporte_gestion.txt"
    )
