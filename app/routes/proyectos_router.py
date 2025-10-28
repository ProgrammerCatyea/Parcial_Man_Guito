from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.proyecto_crud import (
    crear_proyecto,
    obtener_proyectos,
    actualizar_proyecto,
    eliminar_proyecto,
    obtener_proyectos_eliminados,
    generar_reporte_proyectos,
)
from app.schemas.proyecto import ProyectoCreate, ProyectoUpdate, ProyectoResponse
from fastapi.responses import FileResponse

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])

@router.post("/", response_model=ProyectoResponse)
def crear_nuevo_proyecto(proyecto: ProyectoCreate, db: Session = Depends(get_db)):
    return crear_proyecto(db, proyecto)

@router.get("/", response_model=list[ProyectoResponse])
def listar_proyectos(db: Session = Depends(get_db)):
    return obtener_proyectos(db)

@router.put("/{proyecto_id}", response_model=ProyectoResponse)
def editar_proyecto(proyecto_id: int, datos: ProyectoUpdate, db: Session = Depends(get_db)):
    return actualizar_proyecto(db, proyecto_id, datos)

@router.delete("/{proyecto_id}")
def eliminar_proyecto_por_id(proyecto_id: int, db: Session = Depends(get_db)):
    return eliminar_proyecto(db, proyecto_id)

@router.get("/eliminados", response_model=list[ProyectoResponse])
def listar_proyectos_eliminados(db: Session = Depends(get_db)):
    return obtener_proyectos_eliminados(db)

@router.get("/reporte", response_class=FileResponse)
def descargar_reporte_proyectos(db: Session = Depends(get_db)):
    ruta_reporte = generar_reporte_proyectos(db)
    return FileResponse(ruta_reporte, media_type="text/plain", filename="reporte_proyectos.txt")

