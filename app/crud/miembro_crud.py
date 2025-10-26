from sqlalchemy.orm import Session
from app.models.miembro import Miembro
from app.schemas.miembro import MiembroCreate, MiembroUpdate
from typing import List, Optional


def crear_miembro(db: Session, miembro: MiembroCreate):
    """Crea un nuevo miembro si no existe otro con el mismo nombre."""
    existente = db.query(Miembro).filter(Miembro.nombre == miembro.nombre).first()
    if existente:
        return None

    nuevo_miembro = Miembro(
        nombre=miembro.nombre,
        cargo=miembro.cargo,
        especialidad=miembro.especialidad,
        estado=miembro.estado,
    )
    db.add(nuevo_miembro)
    db.commit()
    db.refresh(nuevo_miembro)
    return nuevo_miembro


def listar_miembros(db: Session, especialidad: Optional[str] = None, estado: Optional[str] = None) -> List[Miembro]:
    """Devuelve todos los miembros, con filtros opcionales."""
    query = db.query(Miembro)
    if especialidad:
        query = query.filter(Miembro.especialidad.ilike(f"%{especialidad}%"))
    if estado:
        query = query.filter(Miembro.estado.ilike(f"%{estado}%"))
    return query.all()


def obtener_miembro(db: Session, miembro_id: int) -> Optional[Miembro]:
    """Obtiene un miembro por ID."""
    return db.query(Miembro).filter(Miembro.id == miembro_id).first()


def actualizar_miembro(db: Session, miembro_id: int, miembro: MiembroUpdate):
    """Actualiza los datos de un miembro existente."""
    db_miembro = db.query(Miembro).filter(Miembro.id == miembro_id).first()
    if not db_miembro:
        return None

    for key, value in miembro.dict(exclude_unset=True).items():
        setattr(db_miembro, key, value)

    db.commit()
    db.refresh(db_miembro)
    return db_miembro


def eliminar_miembro(db: Session, miembro_id: int):
    """Elimina un miembro por su ID."""
    db_miembro = db.query(Miembro).filter(Miembro.id == miembro_id).first()
    if not db_miembro:
        return None

    db.delete(db_miembro)
    db.commit()
    return True
