"""Rutas para la gestión de miembros (empleados) en el sistema."""


from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.crud.miembro_crud import listar_miembros, obtener_miembro, crear_miembro, eliminar_miembro, listar_eliminados
from app.core.database import get_db

router = APIRouter(prefix="/miembros", tags=["Miembros"])

@router.get("/", summary="Listar miembros", description="Obtiene todos los miembros con filtros opcionales por estado o especialidad.")
def obtener_miembros(
    estado: str = Query(None, description="Filtrar por estado (Activo o Eliminado)"),
    especialidad: str = Query(None, description="Filtrar por especialidad"),
    db: Session = Depends(get_db)
):
    return listar_miembros(db, estado, especialidad)


@router.get("/eliminados", summary="Listar miembros eliminados", description="Muestra los miembros marcados como eliminados.")
def obtener_miembros_eliminados(db: Session = Depends(get_db)):
    return listar_eliminados(db)


@router.post("/", summary="Crear nuevo miembro", description="Crea un nuevo miembro con nombre, especialidad y salario.")
def crear_nuevo_miembro(nombre: str, especialidad: str, salario: float, db: Session = Depends(get_db)):
    return crear_miembro(db, nombre, especialidad, salario)


@router.delete("/{miembro_id}", summary="Eliminar miembro", description="Elimina un miembro solo si no es gerente de un proyecto activo. Requiere confirmación.")
def eliminar_un_miembro(miembro_id: int, confirm: bool = False, db: Session = Depends(get_db)):
    miembro = obtener_miembro(db, miembro_id)
    if not miembro:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")

    if hasattr(miembro, "proyectos_gerente") and miembro.proyectos_gerente:
        raise HTTPException(status_code=400, detail="No se puede eliminar: este miembro es gerente de un proyecto activo")

    if not confirm:
        return {"mensaje": f"¿Deseas confirmar la eliminación del miembro '{miembro.nombre}'?", "confirmar_con": f"/miembros/{miembro_id}?confirm=true"}

    eliminar_miembro(db, miembro_id)
    return {"mensaje": f"Miembro '{miembro.nombre}' marcado como eliminado correctamente."}

