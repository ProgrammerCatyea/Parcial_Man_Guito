from app.models.asignacion import Asignacion
from sqlalchemy.orm import Session

def listar_asignaciones(db: Session):
    return db.query(Asignacion).all()


def crear_asignacion(db: Session, asignacion):
    nueva_asignacion = Asignacion(**asignacion.model_dump())
    db.add(nueva_asignacion)
    db.commit()
    db.refresh(nueva_asignacion)
    return nueva_asignacion


def obtener_asignacion(db: Session, asignacion_id: int):
    return db.query(Asignacion).filter(Asignacion.id == asignacion_id).first()


def actualizar_asignacion(db: Session, asignacion_id: int, datos):
    asignacion = obtener_asignacion(db, asignacion_id)
    if asignacion:
        for key, value in datos.model_dump().items():
            setattr(asignacion, key, value)
        db.commit()
        db.refresh(asignacion)
    return asignacion


def eliminar_asignacion(db: Session, asignacion_id: int):
    asignacion = obtener_asignacion(db, asignacion_id)
    if asignacion:
        db.delete(asignacion)
        db.commit()
    return asignacion
