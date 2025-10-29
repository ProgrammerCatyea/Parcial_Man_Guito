from sqlalchemy.orm import Session
from app.models.proyecto import Proyecto, EstadoProyecto

def obtener_proyecto(db: Session, proyecto_id: int):
    return db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()

def listar_proyectos(db: Session):
    return db.query(Proyecto).filter(Proyecto.estado != EstadoProyecto.ELIMINADO).all()

def crear_proyecto(db: Session, nombre: str, descripcion: str, presupuesto: float):
    nuevo_proyecto = Proyecto(nombre=nombre, descripcion=descripcion, presupuesto=presupuesto)
    db.add(nuevo_proyecto)
    db.commit()
    db.refresh(nuevo_proyecto)
    return nuevo_proyecto

def eliminar_proyecto(db: Session, proyecto_id: int):
    proyecto = obtener_proyecto(db, proyecto_id)
    if not proyecto:
        return None
    proyecto.estado = EstadoProyecto.ELIMINADO
    db.commit()
    db.refresh(proyecto)
    return proyecto

def listar_eliminados(db: Session):
    return db.query(Proyecto).filter(Proyecto.estado == EstadoProyecto.ELIMINADO).all()
