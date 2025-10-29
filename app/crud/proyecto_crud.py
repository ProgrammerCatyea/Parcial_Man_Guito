"""
Rutas para la gestión de proyectos.
"""
from app.models.proyecto import Proyecto
from sqlalchemy.orm import Session

def listar_proyectos(db: Session, estado: str = None, presupuesto_min: float = None, presupuesto_max: float = None):
    query = db.query(Proyecto)
    if estado:
        query = query.filter(Proyecto.estado.ilike(f"%{estado}%"))
    if presupuesto_min is not None:
        query = query.filter(Proyecto.presupuesto >= presupuesto_min)
    if presupuesto_max is not None:
        query = query.filter(Proyecto.presupuesto <= presupuesto_max)
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
        for key, value in datos.model_dump().items():
            setattr(proyecto, key, value)
        db.commit()
        db.refresh(proyecto)
    return proyecto


def eliminar_proyecto(db: Session, proyecto_id: int):
    proyecto = obtener_proyecto(db, proyecto_id)
    if proyecto:
        proyecto.estado = "Eliminado"
        db.commit()
        db.refresh(proyecto)
    return proyecto


def listar_proyectos_eliminados(db: Session):
    return db.query(Proyecto).filter(Proyecto.estado == "Eliminado").all()
