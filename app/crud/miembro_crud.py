from sqlalchemy.orm import Session
from app.models.miembro import Miembro
from app.schemas.miembro import MiembroCreate, MiembroUpdate


def listar_miembros(db: Session, estado: str = None, especialidad: str = None):
    """
    Devuelve todos los miembros registrados, con opción de filtrar por estado o especialidad.
    """
    query = db.query(Miembro)
    if estado:
        query = query.filter(Miembro.estado.ilike(f"%{estado}%"))
    if especialidad:
        query = query.filter(Miembro.especialidad.ilike(f"%{especialidad}%"))
    return query.all()


def crear_miembro(db: Session, miembro: MiembroCreate):
    """
    Crea un nuevo miembro y lo guarda en la base de datos.
    """
    nuevo_miembro = Miembro(**miembro.model_dump())
    db.add(nuevo_miembro)
    db.commit()
    db.refresh(nuevo_miembro)
    return nuevo_miembro


def obtener_miembro(db: Session, miembro_id: int):
    """
    Retorna un miembro específico por su ID, o None si no existe.
    """
    return db.query(Miembro).filter(Miembro.id == miembro_id).first()


def actualizar_miembro(db: Session, miembro_id: int, datos: MiembroUpdate):
    """
    Actualiza los datos de un miembro existente.
    """
    miembro = obtener_miembro(db, miembro_id)
    if miembro:
        for key, value in datos.model_dump(exclude_unset=True).items():
            setattr(miembro, key, value)
        db.commit()
        db.refresh(miembro)
    return miembro

def eliminar_miembro(db: Session, miembro_id: int):
    """
    Marca un miembro como eliminado sin borrarlo físicamente.
    """
    miembro = obtener_miembro(db, miembro_id)
    if miembro:
        miembro.estado = "Eliminado"
        db.commit()
        db.refresh(miembro)
    return miembro

def listar_miembros_eliminados(db: Session):
    """
    Retorna todos los miembros que fueron marcados como eliminados.
    """
    return db.query(Miembro).filter(Miembro.estado == "Eliminado").all()
