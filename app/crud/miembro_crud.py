from sqlalchemy.orm import Session
from app.models.miembro import Miembro
from app.schemas.miembro import MiembroCreate, MiembroUpdate
from fastapi import HTTPException
from datetime import datetime


def crear_miembro(db: Session, miembro: MiembroCreate):
    nuevo_miembro = Miembro(
        nombre=miembro.nombre,
        correo=miembro.correo,
        rol=miembro.rol
    )
    db.add(nuevo_miembro)
    db.commit()
    db.refresh(nuevo_miembro)
    return nuevo_miembro


def obtener_miembros(db: Session):
    return db.query(Miembro).filter(Miembro.eliminado == False).all()


def actualizar_miembro(db: Session, miembro_id: int, datos: MiembroUpdate):
    miembro = db.query(Miembro).filter(Miembro.id == miembro_id, Miembro.eliminado == False).first()
    if not miembro:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(miembro, key, value)

    db.commit()
    db.refresh(miembro)
    return miembro


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
    contenido = "📋 REPORTE DE MIEMBROS ACTIVOS\n\n"
    for m in miembros:
        contenido += f"ID: {m.id}\nNombre: {m.nombre}\nCorreo: {m.correo}\nRol: {m.rol}\n\n"

    ruta = "data/reporte_miembros.txt"
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)
    return ruta
