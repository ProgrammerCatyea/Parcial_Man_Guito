"""Rutas para asignar y desasignar miembros a proyectos."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.asignacion import AsignacionCreate, AsignacionResponse
from app.crud.asignacion_crud import (
    listar_asignaciones,
    crear_asignacion,
    actualizar_asignacion,
    eliminar_asignacion,
    obtener_asignacion
)

router = APIRouter(prefix="/asignaciones", tags=["Asignaciones"])

@router.get("/", response_model=List[AsignacionResponse])
def listar_todas_asignaciones(db: Session = Depends(get_db)):
    asignaciones = listar_asignaciones(db)
    if not asignaciones:
        raise HTTPException(status_code=404, detail="No se encontraron asignaciones")
    return asignaciones

@router.post("/", response_model=AsignacionResponse)
def crear_una_asignacion(asignacion: AsignacionCreate, db: Session = Depends(get_db)):
    return crear_asignacion(db, asignacion)

@router.put("/{asignacion_id}", response_model=AsignacionResponse)
def actualizar_una_asignacion(asignacion_id: int, asignacion: AsignacionCreate, db: Session = Depends(get_db)):
    existente = obtener_asignacion(db, asignacion_id)
    if not existente:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    return actualizar_asignacion(db, asignacion_id, asignacion)

@router.delete("/{asignacion_id}")
def eliminar_una_asignacion(asignacion_id: int, db: Session = Depends(get_db)):
    asignacion = eliminar_asignacion(db, asignacion_id)
    if not asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    return {"mensaje": f"Asignación {asignacion_id} eliminada correctamente"}
