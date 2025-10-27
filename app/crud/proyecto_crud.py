from sqlalchemy.orm import Session
from app.models.proyecto import Proyecto, ProyectoEliminado
from app.schemas.proyecto import ProyectoCreate, ProyectoUpdate
from datetime import date

def crear_proyecto(db: Session, proyecto: ProyectoCreate):
    nuevo_proyecto = Proyecto(
        nombre=proyecto.nombre,
        descripcion=proyecto.descripcion,
        fecha_inicio=proyecto.fecha_inicio,
        fecha_fin=proyecto.fecha_fin,
        estado=proyecto.estado
    )
    db.add(nuevo_proyecto)
    db.commit()
    db.refresh(nuevo_proyecto)
    return nuevo_proyecto


def obtener_proyectos(db: Session):
    return db.query(Proyecto).all()


def obtener_proyecto_por_id(db: Session, proyecto_id: int):
    return db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()


def actualizar_proyecto(db: Session, proyecto_id: int, proyecto_actualizado: ProyectoUpdate):
    proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()
    if not proyecto:
        return None

    for key, value in proyecto_actualizado.dict(exclude_unset=True).items():
        setattr(proyecto, key, value)

    db.commit()
    db.refresh(proyecto)
    return proyecto


def eliminar_proyecto(db: Session, proyecto_id: int, motivo: str = "Sin motivo especificado"):
    proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()
    if not proyecto:
        return None


    eliminado = ProyectoEliminado(
        nombre=proyecto.nombre,
        descripcion=proyecto.descripcion,
        fecha_inicio=proyecto.fecha_inicio,
        fecha_fin=proyecto.fecha_fin,
        estado=proyecto.estado,
        motivo_eliminacion=motivo
    )

    db.add(eliminado)
    db.delete(proyecto)
    db.commit()
    return eliminado

def obtener_proyectos_eliminados(db: Session):
    return db.query(ProyectoEliminado).all()

def generar_reporte_eliminados(db: Session, ruta_archivo: str = "reporte_proyectos_eliminados.txt"):
    eliminados = db.query(ProyectoEliminado).all()
    if not eliminados:
        return None

    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        archivo.write("=== REPORTE DE PROYECTOS ELIMINADOS ===\n\n")
        for p in eliminados:
            archivo.write(f"ID: {p.id}\n")
            archivo.write(f"Nombre: {p.nombre}\n")
            archivo.write(f"Estado: {p.estado}\n")
            archivo.write(f"Motivo: {p.motivo_eliminacion}\n")
            archivo.write(f"Fecha de inicio: {p.fecha_inicio}\n")
            archivo.write(f"Fecha de fin: {p.fecha_fin}\n")
            archivo.write("-" * 40 + "\n")
    return ruta_archivo
