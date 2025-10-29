from sqlalchemy.orm import Session
from typing import Optional
from app.models.miembro import Miembro

def listar_miembros(
    db: Session,
    especialidad: Optional[str] = None,
    rol: Optional[str] = None,
    nombre: Optional[str] = None
):
    query = db.query(Miembro)
    if especialidad:
        query = query.filter(Miembro.especialidad.ilike(f"%{especialidad}%"))
    if rol:
        query = query.filter(Miembro.rol.ilike(f"%{rol}%"))
    if nombre:
        query = query.filter(Miembro.nombre.ilike(f"%{nombre}%"))
    return query.all()

def obtener_miembro(db: Session, miembro_id: int):
    return db.query(Miembro).filter(Miembro.id == miembro_id).first()

def eliminar_miembro(db: Session, miembro_id: int):
    miembro = obtener_miembro(db, miembro_id)
    if miembro:
        db.delete(miembro)
        db.commit()
        return True
    return False
