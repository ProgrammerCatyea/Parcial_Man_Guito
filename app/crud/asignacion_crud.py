from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
from datetime import date
from app.models.asignacion import Asignacion
from app.models.proyecto import Proyecto
from app.models.miembro import Miembro


def listar_asignaciones(
    db: Session,
    id_proyecto: Optional[int] = None,
    id_miembro: Optional[int] = None
) -> List[Asignacion]:
    query = db.query(Asignacion)
    if id_proyecto:
        query = query.filter(Asignacion.id_proyecto == id_proyecto)
    if id_miembro:
        query = query.filter(Asignacion.id_miembro == id_miembro)
    return query.all()


def crear_asignacion(db: Session, asignacion):
    try:
        
        proyecto = db.query(Proyecto).filter(Proyecto.id == asignacion.id_proyecto).first()
        if not proyecto:
            raise HTTPException(status_code=404, detail="El proyecto no existe.")
        if proyecto.estado == "Eliminado":
            raise HTTPException(status_code=400, detail="No se pueden asignar miembros a un proyecto eliminado.")

        
        miembro = db.query(Miembro).filter(Miembro.id == asignacion.id_miembro).first()
        if not miembro:
            raise HTTPException(status_code=404, detail="El miembro no existe.")
        if miembro.estado == "Eliminado":
            raise HTTPException(status_code=400, detail="No se puede asignar un miembro eliminado.")

       
        existe = db.query(Asignacion).filter(
            Asignacion.id_miembro == asignacion.id_miembro,
            Asignacion.id_proyecto == asignacion.id_proyecto
        ).first()

        if existe:
            raise HTTPException(
                status_code=400,
                detail="El miembro ya está asignado a este proyecto."
            )

      
        nueva_asignacion = Asignacion(**asignacion.model_dump())
        db.add(nueva_asignacion)
        db.commit()
        db.refresh(nueva_asignacion)
        return nueva_asignacion

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad en la base de datos.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear la asignación: {str(e)}")


def obtener_asignacion(db: Session, asignacion_id: int):
    return db.query(Asignacion).filter(Asignacion.id == asignacion_id).first()


def actualizar_asignacion(db: Session, asignacion_id: int, datos):
    asignacion = obtener_asignacion(db, asignacion_id)
    if not asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada.")

    for key, value in datos.model_dump(exclude_unset=True).items():
        setattr(asignacion, key, value)

    db.commit()
    db.refresh(asignacion)
    return asignacion


def eliminar_asignacion(db: Session, asignacion_id: int):
    asignacion = obtener_asignacion(db, asignacion_id)
    if not asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada.")

    db.delete(asignacion)
    db.commit()
    return {"mensaje": f"Asignación {asignacion_id} eliminada correctamente."}
