from sqlalchemy.orm import Session
from ..models.asignacion import Asignacion
from ..models.miembro import Miembro
from ..models.proyecto import Proyecto

def asignar(db: Session, data: dict):
    m = db.get(Miembro, data["miembro_id"])
    p = db.get(Proyecto, data["proyecto_id"])
    if not m:
        return None, "miembro_invalido"
    if not p:
        return None, "proyecto_invalido"
    dup = db.query(Asignacion).filter(
        Asignacion.miembro_id == data["miembro_id"],
        Asignacion.proyecto_id == data["proyecto_id"]
    ).first()
    if dup:
        return None, "duplicada"
    a = Asignacion(**data)
    db.add(a)
    db.commit()
    db.refresh(a)
    return a, None

def desasignar(db: Session, asignacion_id: int):
    a = db.get(Asignacion, asignacion_id)
    if not a:
        return "no_encontrado"
    db.delete(a)
    db.commit()
    return None

def miembros_de_proyecto(db: Session, proyecto_id: int):
    if not db.get(Proyecto, proyecto_id):
        return None, "proyecto_invalido"
    asigs = db.query(Asignacion).filter(Asignacion.proyecto_id == proyecto_id).all()
    return [db.get(Miembro, a.miembro_id) for a in asigs], None

def proyectos_de_miembro(db: Session, miembro_id: int):
    if not db.get(Miembro, miembro_id):
        return None, "miembro_invalido"
    asigs = db.query(Asignacion).filter(Asignacion.miembro_id == miembro_id).all()
    proyectos = [db.get(Proyecto, a.proyecto_id) for a in asigs]
    return proyectos, None
