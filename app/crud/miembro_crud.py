from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.miembro import Miembro
from app.models.proyecto import Proyecto

def obtener_miembros(db: Session, especialidad: str = None, estado: str = None):
    query = db.query(Miembro)

    if especialidad:
        query = query.filter(Miembro.especialidad.ilike(f"%{especialidad}%"))
    if estado:
        query = query.filter(Miembro.estado.ilike(f"%{estado}%"))

    return query.all()

def crear_miembro(db: Session, miembro_data):
    miembro_existente = db.query(Miembro).filter(Miembro.nombre == miembro_data.nombre).first()
    if miembro_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un miembro con ese nombre."
        )

    nuevo_miembro = Miembro(**miembro_data.dict())
    db.add(nuevo_miembro)
    db.commit()
    db.refresh(nuevo_miembro)
    return nuevo_miembro


def actualizar_miembro(db: Session, miembro_id: int, miembro_data):
    miembro = db.query(Miembro).filter(Miembro.id == miembro_id).first()
    if not miembro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Miembro no encontrado."
        )

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


    proyectos_gerenciados = db.query(Proyecto).filter(Proyecto.gerente_id == miembro_id).all()
    if proyectos_gerenciados:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar este miembro porque es gerente de uno o más proyectos activos."
        )

    db.delete(miembro)
    db.commit()
    return {"mensaje": f"Miembro con ID {miembro_id} eliminado correctamente."}

def eliminar_miembro(db: Session, miembro_id: int):
    miembro = db.query(Miembro).filter(Miembro.id == miembro_id, Miembro.eliminado == False).first()
    if not miembro:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")

    miembro.eliminado = True
    miembro.fecha_eliminacion = datetime.now()
    db.commit()
    return {"mensaje": f"Miembro '{miembro.nombre}' eliminado correctamente."}


def obtener_miembros_eliminados(db: Session):
    return db.query(Miembro).filter(Miembro.eliminado == True).all()


def generar_reporte_miembros(db: Session):
    miembros = db.query(Miembro).filter(Miembro.eliminado == False).all()
    contenido = " REPORTE DE MIEMBROS ACTIVOS\n\n"
    for m in miembros:
        contenido += f"ID: {m.id}\nNombre: {m.nombre}\nCorreo: {m.correo}\nRol: {m.rol}\n\n"

    ruta = "data/reporte_miembros.txt"
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)
    return ruta
