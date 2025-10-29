from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.miembro_crud import (
    crear_miembro,
    listar_miembros,
    obtener_miembro,
    actualizar_miembro,
    eliminar_miembro,
)
from app.schemas.miembro import MiembroCreate, MiembroUpdate, MiembroOut

router = APIRouter(prefix="/miembros", tags=["Miembros"])

@router.post("/", response_model=MiembroOut)
def crear_nuevo_miembro(miembro: MiembroCreate, db: Session = Depends(get_db)):
    return crear_miembro(db, miembro)

@router.get("/", response_model=list[MiembroOut])
def listar_todos_miembros(
    especialidad: str | None = None,
    estado: str | None = None,
    db: Session = Depends(get_db),
):
    return listar_miembros(db, especialidad, estado)

@router.get("/{miembro_id}", response_model=MiembroOut)
def obtener_un_miembro(miembro_id: int, db: Session = Depends(get_db)):
    miembro = obtener_miembro(db, miembro_id)
    if not miembro:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    return miembro

@router.put("/{miembro_id}", response_model=MiembroOut)
def actualizar_un_miembro(miembro_id: int, miembro: MiembroUpdate, db: Session = Depends(get_db)):
    return actualizar_miembro(db, miembro_id, miembro)

@router.delete("/{miembro_id}")
def eliminar_un_miembro(
    miembro_id: int,
    confirm: bool = False,
    db: Session = Depends(get_db)
):
    miembro = obtener_miembro(db, miembro_id)
    if not miembro:
        raise HTTPException(
            status_code=404,
            detail="Miembro no encontrado."
        )

    proyectos_gerente = db.query(Proyecto).filter(Proyecto.gerente_id == miembro_id).all()
    if proyectos_gerente:
        raise HTTPException(
            status_code=400,
            detail=f"No se puede eliminar al miembro '{miembro.nombre}' porque es gerente de uno o más proyectos activos."
        )

    if not confirm:
        return {
            "mensaje": f"¿Deseas confirmar la eliminación del miembro '{miembro.nombre}'?",
            "confirmar_con": f"/miembros/{miembro_id}?confirm=true"
        }

    eliminar_miembro(db, miembro_id)
    return {"mensaje": f"Miembro '{miembro.nombre}' eliminado correctamente."}
