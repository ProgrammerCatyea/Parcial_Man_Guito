from sqlalchemy.orm import Session
from app.models.proyecto import Proyecto
from app.schemas.proyecto import ProyectoCreate, ProyectoUpdate


def crear_proyecto(db: Session, proyecto: ProyectoCreate):
    nuevo = Proyecto(
        nombre=proyecto.nombre,
        descripcion=proyecto.descripcion,
        estado=proyecto.estado,
        presupuesto=proyecto.presupuesto,
        fecha_inicio=proyecto.fecha_inicio,
        fecha_fin=proyecto.fecha_fin,
        gerente_id=proyecto.gerente_id
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def listar_proyectos(db: Session, estado: str | None = None, presupuesto_min: float | None = None, presupuesto_max: float | None = None):
    query = db.query(Proyecto)
    if estado:
        query = query.filter(Proyecto.estado == estado)
    if presupuesto_min:
        query = query.filter(Proyecto.presupuesto >= presupuesto_min)
    if presupuesto_max:
        query = query.filter(Proyecto.presupuesto <= presupuesto_max)
    return query.all()

def obtener_proyecto(db: Session, proyecto_id: int):
    return db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()

def actualizar_proyecto(db: Session, proyecto_id: int, proyecto_data: ProyectoUpdate):
    proyecto = obtener_proyecto(db, proyecto_id)
    if not proyecto:
        return None
    for key, value in proyecto_data.dict(exclude_unset=True).items():
        setattr(proyecto, key, value)
    db.commit()
    db.refresh(proyecto)
    return proyecto

def eliminar_proyecto(db: Session, proyecto_id: int):
    proyecto = obtener_proyecto(db, proyecto_id)
    if not proyecto:
        return None
    db.delete(proyecto)
    db.commit()
    return proyecto
