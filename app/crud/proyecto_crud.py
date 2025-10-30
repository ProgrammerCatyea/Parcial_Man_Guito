"""
Rutas para la gestión de proyectos.
"""
from app.models.proyecto import Proyecto
from sqlalchemy.orm import Session


def listar_proyectos(db: Session, estado: str = None, presupuesto_min: float = None):
    query = db.query(Proyecto)
    if estado:
        query = query.filter(Proyecto.estado.ilike(f"%{estado}%"))
    if presupuesto_min:
        query = query.filter(Proyecto.presupuesto >= presupuesto_min)
    return query.all()

def crear_proyecto(db: Session, proyecto):
    nuevo_proyecto = Proyecto(**proyecto.model_dump())
    db.add(nuevo_proyecto)
    db.commit()
    db.refresh(nuevo_proyecto)
    return nuevo_proyecto

def obtener_proyecto(db: Session, proyecto_id: int):
    return db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()


def actualizar_proyecto(db: Session, proyecto_id: int, datos):
    proyecto = obtener_proyecto(db, proyecto_id)
    if proyecto:
        for key, value in datos.model_dump(exclude_unset=True).items():
            setattr(proyecto, key, value)
        db.commit()
        db.refresh(proyecto)
    return proyecto


def eliminar_proyecto(db: Session, proyecto_id: int):
    proyecto = obtener_proyecto(db, proyecto_id)
    if not proyecto:
        return None
    asignaciones_activas = db.query(Asignacion).filter(
        Asignacion.id_proyecto == proyecto_id
    ).count()

    if asignaciones_activas > 0:
        raise HTTPException(
            status_code=400,
            detail=f"No se puede eliminar el proyecto '{proyecto.nombre}' porque tiene empleados asignados."
        )

    proyecto.estado = "Eliminado"
    db.commit()
    db.refresh(proyecto)
    return proyecto


def listar_proyectos_eliminados(db: Session):

    return db.query(Proyecto).filter(Proyecto.estado == "Eliminado").all()

def listar_proyectos_activos(db: Session):

    return db.query(Proyecto).filter(Proyecto.estado == "Activo").all()
