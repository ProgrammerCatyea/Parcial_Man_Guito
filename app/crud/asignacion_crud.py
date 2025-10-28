from sqlalchemy.orm import Session
from app.models.asignacion import Asignacion
from app.models.miembro import Miembro
from app.models.proyecto import Proyecto
from app.schemas.asignacion import AsignacionCreate
from fastapi import HTTPException
from datetime import datetime


def crear_asignacion(db: Session, asignacion: AsignacionCreate):
    miembro = db.query(Miembro).filter(Miembro.id == asignacion.miembro_id, Miembro.eliminado == False).first()
    proyecto = db.query(Proyecto).filter(Proyecto.id == asignacion.proyecto_id, Proyecto.eliminado == False).first()

    if not miembro or not proyecto:
        raise HTTPException(status_code=404, detail="Miembro o proyecto no encontrado o eliminado")

    nueva_asignacion = Asignacion(
        miembro_id=asignacion.miembro_id,
        proyecto_id=asignacion.proyecto_id,
        fecha_asignacion=datetime.now(),
    )

    db.add(nueva_asignacion)
    db.commit()
    db.refresh(nueva_asignacion)
    return nueva_asignacion


def obtener_asignaciones(db: Session):
    return db.query(Asignacion).filter(Asignacion.eliminado == False).all()


def eliminar_asignacion(db: Session, asignacion_id: int):
    asignacion = db.query(Asignacion).filter(Asignacion.id == asignacion_id, Asignacion.eliminado == False).first()
    if not asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")

    asignacion.eliminado = True
    asignacion.fecha_eliminacion = datetime.now()
    db.commit()
    return {"mensaje": f"Asignación ID {asignacion.id} eliminada correctamente."}


def obtener_asignaciones_eliminadas(db: Session):
    return db.query(Asignacion).filter(Asignacion.eliminado == True).all()


def generar_reporte_asignaciones(db: Session):
    asignaciones = db.query(Asignacion).filter(Asignacion.eliminado == False).all()
    contenido = "🧩 REPORTE DE ASIGNACIONES ACTIVAS\n\n"

    for a in asignaciones:
        miembro = db.query(Miembro).filter(Miembro.id == a.miembro_id).first()
        proyecto = db.query(Proyecto).filter(Proyecto.id == a.proyecto_id).first()
        contenido += (
            f"Asignación ID: {a.id}\n"
            f"Miembro: {miembro.nombre if miembro else 'Desconocido'}\n"
            f"Proyecto: {proyecto.nombre if proyecto else 'Desconocido'}\n"
            f"Fecha Asignación: {a.fecha_asignacion}\n\n"
        )

    ruta = "data/reporte_asignaciones.txt"
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)
    return ruta
