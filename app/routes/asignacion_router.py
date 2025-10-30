"""Rutas para asignar y desasignar miembros a proyectos."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.asignacion import (
    AsignacionCreate,
    AsignacionUpdate,
    AsignacionResponse
)
from app.crud.asignacion_crud import (
    listar_asignaciones,
    crear_asignacion,
    actualizar_asignacion,
    eliminar_asignacion,
    obtener_asignacion
)

router = APIRouter(prefix="/asignaciones", tags=["Asignaciones"])

@router.get("/", response_model=List[AsignacionResponse])
def listar_todas_asignaciones(
    id_proyecto: Optional[int] = Query(None, description="Filtrar por ID de proyecto"),
    id_miembro: Optional[int] = Query(None, description="Filtrar por ID de miembro"),
    db: Session = Depends(get_db)
):

    asignaciones = listar_asignaciones(db, id_proyecto=id_proyecto, id_miembro=id_miembro)
    if not asignaciones:
        raise HTTPException(status_code=404, detail="No se encontraron asignaciones registradas.")
    return asignaciones


@router.post("/", response_model=AsignacionResponse)
def crear_una_asignacion(asignacion: AsignacionCreate, db: Session = Depends(get_db)):
    nueva_asignacion = crear_asignacion(db, asignacion)
    if not nueva_asignacion:
        raise HTTPException(status_code=400, detail="El miembro ya está asignado a este proyecto.")
    return nueva_asignacion



@router.put("/{asignacion_id}", response_model=AsignacionResponse)
def actualizar_una_asignacion(asignacion_id: int, datos: AsignacionUpdate, db: Session = Depends(get_db)):
    existente = obtener_asignacion(db, asignacion_id)
    if not existente:
        raise HTTPException(status_code=404, detail="Asignación no encontrada.")
    return actualizar_asignacion(db, asignacion_id, datos)

@router.delete("/{asignacion_id}")
def eliminar_una_asignacion(asignacion_id: int, db: Session = Depends(get_db)):
  
    resultado = eliminar_asignacion(db, asignacion_id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Asignación no encontrada.")
    return {"mensaje": f"La asignación con ID {asignacion_id} fue eliminada correctamente."}
