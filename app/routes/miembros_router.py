from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.miembro import Miembro
from app.schemas.miembro import MiembroCreate, MiembroUpdate, MiembroResponse
from app.crud.miembro_crud import (
    crear_miembro,
    obtener_miembro,
    listar_miembros,
    actualizar_miembro,
    eliminar_miembro
)

router = APIRouter(
    prefix="/miembros",
    tags=["Miembros"]
)


@router.post("/", response_model=MiembroResponse, status_code=201)
def crear_nuevo_miembro(miembro: MiembroCreate, db: Session = Depends(get_db)):
    """Crea un nuevo miembro en la base de datos."""
    db_miembro = crear_miembro(db, miembro)
    if not db_miembro:
        raise HTTPException(status_code=400, detail="Ya existe un miembro con ese nombre.")
    return db_miembro


@router.get("/", response_model=List[MiembroResponse])
def listar_todos_los_miembros(
    especialidad: Optional[str] = Query(None, description="Filtrar por especialidad"),
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    db: Session = Depends(get_db)
):
    """Lista todos los miembros, con filtros opcionales."""
    miembros = listar_miembros(db, especialidad, estado)
    return miembros


@router.get("/{miembro_id}", response_model=MiembroResponse)
def obtener_miembro_por_id(miembro_id: int, db: Session = Depends(get_db)):
    """Obtiene un miembro por su ID."""
    db_miembro = obtener_miembro(db, miembro_id)
    if not db_miembro:
        raise HTTPException(status_code=404, detail="Miembro no encontrado.")
    return db_miembro


@router.put("/{miembro_id}", response_model=MiembroResponse)
def actualizar_miembro_por_id(
    miembro_id: int, 
    miembro: MiembroUpdate, 
    db: Session = Depends(get_db)
):
    """Actualiza los datos de un miembro existente."""
    db_miembro = actualizar_miembro(db, miembro_id, miembro)
    if not db_miembro:
        raise HTTPException(status_code=404, detail="No se pudo actualizar el miembro.")
    return db_miembro


@router.delete("/{miembro_id}", status_code=204)
def eliminar_miembro_por_id(miembro_id: int, db: Session = Depends(get_db)):
    """Elimina un miembro de la base de datos."""
    eliminado = eliminar_miembro(db, miembro_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Miembro no encontrado o no se puede eliminar.")
    return {"mensaje": "Miembro eliminado correctamente"}
