"""Rutas para la gestión de miembros (empleados) en el sistema."""


from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.miembro import MiembroCreate, MiembroUpdate, MiembroResponse
from app.crud.miembro_crud import (
    crear_miembro,
    obtener_miembro,
    listar_miembros,
    actualizar_miembro,
    eliminar_miembro,
    listar_miembros_eliminados
)

router = APIRouter(prefix="/miembros", tags=["Miembros"])





@router.get("/", response_model=List[MiembroResponse])
def listar_todos_los_miembros(
    estado: Optional[str] = Query(None, description="Filtrar por estado (Activo/Inactivo)"),
    especialidad: Optional[str] = Query(None, description="Filtrar por especialidad"),
    db: Session = Depends(get_db)
):
    miembros = listar_miembros(db, estado=estado, especialidad=especialidad)
    if not miembros:
        raise HTTPException(status_code=404, detail="No se encontraron miembros con los filtros aplicados")
    return miembros



@router.post("/", response_model=MiembroResponse)
def crear_un_miembro(miembro: MiembroCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo miembro en la base de datos.
    """
    return crear_miembro(db, miembro)



@router.put("/{miembro_id}", response_model=MiembroResponse)
def actualizar_un_miembro(miembro_id: int, miembro: MiembroUpdate, db: Session = Depends(get_db)):

    miembro_existente = obtener_miembro(db, miembro_id)
    if not miembro_existente:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    return actualizar_miembro(db, miembro_id, miembro)



@router.delete("/{miembro_id}")
def eliminar_un_miembro(miembro_id: int, confirm: bool = False, db: Session = Depends(get_db)):

    miembro = obtener_miembro(db, miembro_id)
    if not miembro:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")

    if hasattr(miembro, "proyectos_gerente") and miembro.proyectos_gerente:
        raise HTTPException(status_code=400, detail="No se puede eliminar: este miembro es gerente de un proyecto activo")

    if not confirm:
        return {
            "mensaje": f"¿Deseas confirmar la eliminación del miembro '{miembro.nombre}'?",
            "confirmar_con": f"/miembros/{miembro_id}?confirm=true"
        }

    eliminar_miembro(db, miembro_id)
    return {"mensaje": f"Miembro '{miembro.nombre}' eliminado correctamente."}


@router.get("/eliminados", response_model=List[MiembroResponse])
def listar_miembros_eliminados_endpoint(db: Session = Depends(get_db)):

    eliminados = listar_miembros_eliminados(db)
    if not eliminados:
        raise HTTPException(status_code=404, detail="No hay miembros eliminados registrados")
    return eliminados
