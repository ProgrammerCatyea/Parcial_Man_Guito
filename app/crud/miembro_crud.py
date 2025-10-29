from sqlalchemy.orm import Session
from app.models.miembro import Miembro
from app.schemas.miembro import MiembroCreate, MiembroUpdate


def crear_miembro(db: Session, miembro: MiembroCreate):
    nuevo = Miembro(
        nombre=miembro.nombre,
        correo=miembro.correo,
        rol=miembro.rol,
        activo=miembro.activo
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def listar_miembros(db: Session):
    return db.query(Miembro).all()

def obtener_miembro(db: Session, miembro_id: int):
    return db.query(Miembro).filter(Miembro.id == miembro_id).first()


def actualizar_miembro(db: Session, miembro_id: int, miembro_data: MiembroUpdate):
    miembro = obtener_miembro(db, miembro_id)
    if not miembro:
        return None
    for key, value in miembro_data.dict(exclude_unset=True).items():
        setattr(miembro, key, value)
    db.commit()
    db.refresh(miembro)
    return miembro


def eliminar_miembro(db: Session, miembro_id: int):
 
    miembro = db.query(Miembro).filter(Miembro.id == miembro_id).first()

    if not miembro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El miembro no existe."
        )

   
    proyectos_gerente = db.query(Proyecto).filter(Proyecto.gerente_id == miembro_id).all()

    if proyectos_gerente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"No se puede eliminar al miembro '{miembro.nombre}' porque es gerente de uno o más proyectos activos."
        )


    db.delete(miembro)
    db.commit()
    return {"message": f"Miembro '{miembro.nombre}' eliminado exitosamente."}