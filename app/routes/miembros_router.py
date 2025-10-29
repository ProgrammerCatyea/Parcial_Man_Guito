from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.miembro_crud import listar_miembros, obtener_miembro, eliminar_miembro
from app.models.proyecto import Proyecto

router = APIRouter()

@router.get("/")
def obtener_miembros(
    especialidad: Optional[str] = Query(None, description="Filtrar por especialidad"),
    rol: Optional[str] = Query(None, description="Filtrar por rol"),
    nombre: Optional[str] = Query(None, description="Buscar por nombre"),
    db: Session = Depends(get_db)
):
    return listar_miembros(db, especialidad, rol, nombre)

@router.delete("/{miembro_id}")
def eliminar_un_miembro(miembro_id: int, confirm: bool = False, db: Session = Depends(get_db)):
    miembro = obtener_miembro(db, miembro_id)
    if not miembro:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")

    proyectos_gerente = db.query(Proyecto).filter(Proyecto.gerente_id == miembro_id).all()
    if proyectos_gerente:
        raise HTTPException(
            status_code=400,
            detail=f"No se puede eliminar al miembro '{miembro.nombre}' porque es gerente de un proyecto activo."
        )

    if not confirm:
        return {
            "mensaje": f"¿Deseas confirmar la eliminación del miembro '{miembro.nombre}'?",
            "confirmar_con": f"/miembros/{miembro_id}?confirm=true"
        }

    eliminar_miembro(db, miembro_id)
    return {"mensaje": f"Miembro '{miembro.nombre}' eliminado correctamente."}

