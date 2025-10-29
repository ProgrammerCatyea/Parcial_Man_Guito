"""Rutas para la administración de proyectos, con filtrado y control de estado."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.proyecto import ProyectoCreate, ProyectoUpdate, ProyectoResponse
from app.crud.proyecto_crud import (
    listar_proyectos,
    crear_proyecto,
    obtener_proyecto,
    actualizar_proyecto,
    eliminar_proyecto,
    listar_proyectos_eliminados
)

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])

@router.get("/", response_model=List[ProyectoResponse])
def listar_proyectos_endpoint(
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    presupuesto_min: Optional[float] = Query(None, description="Filtrar por presupuesto mínimo"),
    db: Session = Depends(get_db)
):
    proyectos = listar_proyectos(db, estado=estado, presupuesto_min=presupuesto_min)
    if not proyectos:
        raise HTTPException(status_code=404, detail="No se encontraron proyectos con los filtros aplicados")
    return proyectos

@router.post("/", response_model=ProyectoResponse)
def crear_proyecto_endpoint(proyecto: ProyectoCreate, db: Session = Depends(get_db)):
    return crear_proyecto(db, proyecto)

@router.put("/{proyecto_id}", response_model=ProyectoResponse)
def actualizar_proyecto_endpoint(proyecto_id: int, datos: ProyectoUpdate, db: Session = Depends(get_db)):
    proyecto_existente = obtener_proyecto(db, proyecto_id)
    if not proyecto_existente:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return actualizar_proyecto(db, proyecto_id, datos)

@router.delete("/{proyecto_id}")
def eliminar_proyecto_endpoint(proyecto_id: int, db: Session = Depends(get_db)):
    proyecto = eliminar_proyecto(db, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return {"mensaje": f"Proyecto '{proyecto.nombre}' marcado como eliminado"}

@router.get("/eliminados", response_model=List[ProyectoResponse])
def listar_eliminados_endpoint(db: Session = Depends(get_db)):
    return listar_proyectos_eliminados(db)
