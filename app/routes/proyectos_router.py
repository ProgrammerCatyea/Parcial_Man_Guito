"""Rutas para la administración de proyectos, con filtrado y control de estado."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.crud.proyecto_crud import listar_proyectos, obtener_proyecto, crear_proyecto, eliminar_proyecto, listar_eliminados
from app.core.database import get_db

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])

@router.get("/", summary="Listar proyectos", description="Obtiene todos los proyectos con filtros opcionales por estado o presupuesto.")
def obtener_proyectos(
    estado: str = Query(None, description="Filtrar por estado (En progreso, Finalizado o Eliminado)"),
    presupuesto_min: float = Query(None, description="Filtrar proyectos con presupuesto mayor o igual a este valor"),
    presupuesto_max: float = Query(None, description="Filtrar proyectos con presupuesto menor o igual a este valor"),
    db: Session = Depends(get_db)
):
    return listar_proyectos(db, estado, presupuesto_min, presupuesto_max)


@router.get("/eliminados", summary="Listar proyectos eliminados", description="Muestra los proyectos marcados como eliminados.")
def obtener_proyectos_eliminados(db: Session = Depends(get_db)):
    return listar_eliminados(db)


@router.post("/", summary="Crear nuevo proyecto", description="Crea un nuevo proyecto con nombre, descripción y presupuesto.")
def crear_nuevo_proyecto(nombre: str, descripcion: str, presupuesto: float, db: Session = Depends(get_db)):
    return crear_proyecto(db, nombre, descripcion, presupuesto)


@router.delete("/{proyecto_id}", summary="Eliminar proyecto", description="Marca un proyecto como eliminado. Requiere confirmación previa.")
def eliminar_un_proyecto(proyecto_id: int, confirm: bool = False, db: Session = Depends(get_db)):
    proyecto = obtener_proyecto(db, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    if not confirm:
        return {"mensaje": f"¿Deseas confirmar la eliminación del proyecto '{proyecto.nombre}'?", "confirmar_con": f"/proyectos/{proyecto_id}?confirm=true"}

    eliminar_proyecto(db, proyecto_id)
    return {"mensaje": f"Proyecto '{proyecto.nombre}' marcado como eliminado correctamente."}
