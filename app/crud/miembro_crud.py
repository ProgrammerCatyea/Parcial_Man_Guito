from app.models.miembro import Miembro
from sqlalchemy.orm import Session
from sqlalchemy import and_


def listar_miembros(db: Session, estado: str = None, especialidad: str = None):
  
    query = db.query(Miembro)

    if estado:
        query = query.filter(Miembro.estado.ilike(f"%{estado}%"))
    if especialidad:
        query = query.filter(Miembro.especialidad.ilike(f"%{especialidad}%"))

    return query.all()

def crear_miembro(db: Session, miembro):
   
    existente = db.query(Miembro).filter(
        and_(
            Miembro.nombre.ilike(miembro.nombre),
            Miembro.estado != "Eliminado"
        )
    ).first()

    if existente:
        raise ValueError(f"Ya existe un miembro activo con el nombre '{miembro.nombre}'")

    nuevo_miembro = Miembro(**miembro.model_dump())
    db.add(nuevo_miembro)
    db.commit()
    db.refresh(nuevo_miembro)
    return nuevo_miembro

def obtener_miembro(db: Session, miembro_id: int):
  
    return db.query(Miembro).filter(Miembro.id == miembro_id).first()

def actualizar_miembro(db: Session, miembro_id: int, datos):
 
    miembro = obtener_miembro(db, miembro_id)
    if miembro:
        for key, value in datos.model_dump().items():
            if value is not None:
                setattr(miembro, key, value)
        db.commit()
        db.refresh(miembro)
    return miembro

def eliminar_miembro(db: Session, miembro_id: int):
  
    miembro = obtener_miembro(db, miembro_id)
    if miembro:
        miembro.estado = "Eliminado"
        db.commit()
        db.refresh(miembro)
    return miembro

def listar_miembros_eliminados(db: Session):
    
    
    return db.query(Miembro).filter(Miembro.estado == "Eliminado").all()
