from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.proyecto_crud import (
    crear_proyecto,
    listar_proyectos,
    obtener_proyecto,
    actualizar_proyecto,
    eliminar_proyecto,
)
from app.schemas.proyecto import ProyectoCreate, ProyectoUpdate, ProyectoOut

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])

@router.post("/", response_model=ProyectoOut)
def crear_nuevo_proyecto(proyecto: ProyectoCreate, db: Session = Depends(get_db)):
    return crear_proyecto(db, proyecto)

@router.get("/", response_model=list[ProyectoOut])
def listar_todos_proyectos(
    estado: str | None = None,
    presupuesto_min: float | None = None,
    presupuesto_max: float | None = None,
    db: Session = Depends(get_db),
):
    return listar_proyectos(db, estado, presupuesto_min, presupuesto_max)

@router.get("/{proyecto_id}", response_model=ProyectoOut)
def obtener_un_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    proyecto = obtener_proyecto(db, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return proyecto

@router.put("/{proyecto_id}", response_model=ProyectoOut)
def actualizar_un_proyecto(proyecto_id: int, proyecto: ProyectoUpdate, db: Session = Depends(get_db)):
    return actualizar_proyecto(db, proyecto_id, proyecto)

@router.delete("/{proyecto_id}")
def eliminar_un_proyecto(proyecto_id: int, confirm: bool = False, db: Session = Depends(get_db)):
    proyecto = obtener_proyecto(db, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    if not confirm:
        return {"mensaje": f"¿Deseas confirmar la eliminación del proyecto '{proyecto.nombre}'?", "confirmar_con": f"/proyectos/{proyecto_id}?confirm=true"}

    eliminar_proyecto(db, proyecto_id)
    return {"mensaje": f"Proyecto '{proyecto.nombre}' eliminado correctamente."}

