from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.proyecto import Proyecto
from app.schemas.proyecto import ProyectoCreate, ProyectoUpdate, ProyectoResponse
from app.crud.proyecto_crud import (
    crear_proyecto,
    listar_proyectos,
    obtener_proyecto,
    actualizar_proyecto,
    eliminar_proyecto
)

router = APIRouter(
    prefix="/proyectos",
    tags=["Proyectos"]
)


@router.post("/", response_model=ProyectoResponse, status_code=201)
def crear_nuevo_proyecto(proyecto: ProyectoCreate, db: Session = Depends(get_db)):
    """Crea un nuevo proyecto si no existe otro con el mismo nombre."""
    db_proyecto = crear_proyecto(db, proyecto)
    if not db_proyecto:
        raise HTTPException(status_code=400, detail="Ya existe un proyecto con ese nombre.")
    return db_proyecto


@router.get("/", response_model=List[ProyectoResponse])
def listar_todos_los_proyectos(
    estado: Optional[str] = Query(None, description="Filtrar por estado del proyecto"),
    db: Session = Depends(get_db)
):
    """Lista todos los proyectos, con filtros opcionales."""
    proyectos = listar_proyectos(db, estado)
    return proyectos


@router.get("/{proyecto_id}", response_model=ProyectoResponse)
def obtener_proyecto_por_id(proyecto_id: int, db: Session = Depends(get_db)):
    """Obtiene un proyecto por su ID."""
    proyecto = obtener_proyecto(db, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado.")
    return proyecto


@router.put("/{proyecto_id}", response_model=ProyectoResponse)
def actualizar_proyecto_por_id(proyecto_id: int, proyecto: ProyectoUpdate, db: Session = Depends(get_db)):
    """Actualiza los datos de un proyecto."""
    actualizado = actualizar_proyecto(db, proyecto_id, proyecto)
    if not actualizado:
        raise HTTPException(status_code=404, detail="No se pudo actualizar el proyecto.")
    return actualizado


@router.delete("/{proyecto_id}", status_code=204)
def eliminar_proyecto_por_id(proyecto_id: int, db: Session = Depends(get_db)):
    """Elimina un proyecto existente."""
    eliminado = eliminar_proyecto(db, proyecto_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado.")
    return {"mensaje": "Proyecto eliminado correctamente"}
