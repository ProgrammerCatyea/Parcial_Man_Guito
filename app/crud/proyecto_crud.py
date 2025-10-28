from sqlalchemy.orm import Session
from app.models.proyecto import Proyecto
from app.schemas.proyecto import ProyectoCreate, ProyectoUpdate
from fastapi import HTTPException
from datetime import datetime


def crear_proyecto(db: Session, proyecto: ProyectoCreate):
    nuevo_proyecto = Proyecto(
        nombre=proyecto.nombre,
        descripcion=proyecto.descripcion,
        fecha_inicio=proyecto.fecha_inicio,
        fecha_fin=proyecto.fecha_fin
    )
    db.add(nuevo_proyecto)
    db.commit()
    db.refresh(nuevo_proyecto)
    return nuevo_proyecto

def obtener_proyectos(db: Session):
    return db.query(Proyecto).filter(Proyecto.eliminado == False).all()

def actualizar_proyecto(db: Session, proyecto_id: int, datos: ProyectoUpdate):
    proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id, Proyecto.eliminado == False).first()
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(proyecto, key, value)

    db.commit()
    db.refresh(proyecto)
    return proyecto


def eliminar_proyecto(db: Session, proyecto_id: int):
    proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id, Proyecto.eliminado == False).first()
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    proyecto.eliminado = True
    proyecto.fecha_eliminacion = datetime.now()
    db.commit()
    return {"mensaje": f"Proyecto '{proyecto.nombre}' eliminado correctamente."}


def obtener_proyectos_eliminados(db: Session):
    return db.query(Proyecto).filter(Proyecto.eliminado == True).all()


def generar_reporte_proyectos(db: Session):
    proyectos = db.query(Proyecto).filter(Proyecto.eliminado == False).all()
    contenido = "📁 REPORTE DE PROYECTOS ACTIVOS\n\n"
    for p in proyectos:
        contenido += (
            f"ID: {p.id}\n"
            f"Nombre: {p.nombre}\n"
            f"Descripción: {p.descripcion}\n"
            f"Inicio: {p.fecha_inicio}\n"
            f"Fin: {p.fecha_fin}\n\n"
        )

    ruta = "data/reporte_proyectos.txt"
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)
    return ruta
