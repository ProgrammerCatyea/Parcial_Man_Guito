from sqlalchemy.orm import Session
from app.models.proyecto import Proyecto, EstadoProyecto
from app.schemas.proyecto import ProyectoCreate, ProyectoUpdate
from datetime import date


def crear_proyecto(db: Session, proyecto_data: ProyectoCreate):
    """Crea un nuevo proyecto si no existe otro con el mismo nombre."""
    existente = db.query(Proyecto).filter(Proyecto.nombre == proyecto_data.nombre).first()
    if existente:
        return None

    nuevo_proyecto = Proyecto(
        nombre=proyecto_data.nombre,
        descripcion=proyecto_data.descripcion,
        fecha_inicio=proyecto_data.fecha_inicio or date.today(),
        fecha_fin=proyecto_data.fecha_fin,
        estado=proyecto_data.estado or EstadoProyecto.PLANIFICADO
    )

    db.add(nuevo_proyecto)
    db.commit()
    db.refresh(nuevo_proyecto)
    return nuevo_proyecto


def listar_proyectos(db: Session, estado: str | None = None):
    """Lista todos los proyectos, con opción de filtrar por estado."""
    query = db.query(Proyecto)
    if estado:
        query = query.filter(Proyecto.estado == estado)
    return query.all()



def obtener_proyecto(db: Session, proyecto_id: int):
    """Obtiene un proyecto por su ID."""
    return db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()



def actualizar_proyecto(db: Session, proyecto_id: int, proyecto_data: ProyectoUpdate):
    """Actualiza los datos de un proyecto existente."""
    proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()
    if not proyecto:
        return None

    for key, value in proyecto_data.model_dump(exclude_unset=True).items():
        setattr(proyecto, key, value)

    db.commit()
    db.refresh(proyecto)
    return proyecto


def eliminar_proyecto(db: Session, proyecto_id: int):
    """Elimina un proyecto de la base de datos."""
    proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()
    if not proyecto:
        return None

    db.delete(proyecto)
    db.commit()
    return proyecto
