from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.proyecto_crud import listar_proyectos, obtener_proyecto, crear_proyecto, eliminar_proyecto, listar_eliminados
from app.core.database import get_db

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])

@router.get("/")
def obtener_proyectos(db: Session = Depends(get_db)):
    return listar_proyectos(db)

@router.get("/eliminados")
def obtener_proyectos_eliminados(db: Session = Depends(get_db)):
    return listar_eliminados(db)

@router.post("/")
def crear_nuevo_proyecto(nombre: str, descripcion: str, presupuesto: float, db: Session = Depends(get_db)):
    return crear_proyecto(db, nombre, descripcion, presupuesto)

@router.delete("/{proyecto_id}")
def eliminar_un_proyecto(proyecto_id: int, confirm: bool = False, db: Session = Depends(get_db)):
    proyecto = obtener_proyecto(db, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    if not confirm:
        return {"mensaje": f"¿Deseas confirmar la eliminación del proyecto '{proyecto.nombre}'?", "confirmar_con": f"/proyectos/{proyecto_id}?confirm=true"}

    eliminar_proyecto(db, proyecto_id)
    return {"mensaje": f"Proyecto '{proyecto.nombre}' marcado como eliminado correctamente."}
