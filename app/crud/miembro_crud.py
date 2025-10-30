from sqlalchemy.orm import Session
from app.models.miembro import Miembro

def listar_miembros(db: Session, estado: str = None, especialidad: str = None):
 
    query = db.query(Miembro)
    if estado:
        query = query.filter(Miembro.estado.ilike(f"%{estado}%"))
    if especialidad:
        query = query.filter(Miembro.especialidad.ilike(f"%{especialidad}%"))
    return query.all()



def obtener_miembro(db: Session, miembro_id: int):
   
    return db.query(Miembro).filter(Miembro.id == miembro_id).first()


def crear_miembro(db: Session, miembro):

    nuevo_miembro = Miembro(**miembro.model_dump())
    db.add(nuevo_miembro)
    db.commit()
    db.refresh(nuevo_miembro)
    return nuevo_miembro


def actualizar_miembro(db: Session, miembro_id: int, datos):

    miembro = obtener_miembro(db, miembro_id)
    if miembro:
        for key, value in datos.model_dump(exclude_unset=True).items():
            setattr(miembro, key, value)
        db.commit()
        db.refresh(miembro)
    return miembro



def eliminar_miembro(db: Session, miembro_id: int):
  
    miembro = db.query(Miembro).filter(Miembro.id == miembro_id).first()

    if not miembro:
        return None

    proyectos_activos = db.query(Proyecto).filter(
        Proyecto.id_gerente == miembro_id,
        Proyecto.estado == "Activo"
    ).count()

    if proyectos_activos > 0:
        raise HTTPException(
            status_code=400,
            detail=f"No se puede eliminar: el miembro '{miembro.nombre}' es gerente de un proyecto activo."
        )

    miembro.estado = "Eliminado"
    db.commit()
    db.refresh(miembro)
    return miembro




def listar_miembros_eliminados(db: Session):

    return db.query(Miembro).filter(Miembro.estado == "Eliminado").all()
