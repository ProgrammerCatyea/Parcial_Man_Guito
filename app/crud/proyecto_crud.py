"""
Rutas para la gestión de proyectos.
"""
from app.models.proyecto import Proyecto
from sqlalchemy.orm import Session

def listar_proyectos(db: Session, estado: str = None, presupuesto_min: float = None):
    """
    Lista todos los proyectos. Puede filtrar por estado y por presupuesto mínimo.
    """
    query = db.query(Proyecto)
    if estado:
        query = query.filter(Proyecto.estado.ilike(f"%{estado}%"))
    if presupuesto_min:
        query = query.filter(Proyecto.presupuesto >= presupuesto_min)
    return query.all()


def crear_proyecto(db: Session, proyecto):
    """
    Crea un nuevo proyecto a partir del esquema recibido.
    """
    nuevo_proyecto = Proyecto(**proyecto.model_dump())
    db.add(nuevo_proyecto)
    db.commit()
    db.refresh(nuevo_proyecto)
    return nuevo_proyecto


def obtener_proyecto(db: Session, proyecto_id: int):
    """
    Obtiene un proyecto específico por su ID.
    """
    return db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()


def actualizar_proyecto(db: Session, proyecto_id: int, datos):
    """
    Actualiza la información de un proyecto existente.
    """
    proyecto = obtener_proyecto(db, proyecto_id)
    if proyecto:
        for key, value in datos.model_dump().items():
            setattr(proyecto, key, value)
        db.commit()
        db.refresh(proyecto)
    return proyecto


def eliminar_proyecto(db: Session, proyecto_id: int):
    """
    Marca un proyecto como 'Eliminado' sin borrarlo físicamente de la base de datos.
    """
    proyecto = obtener_proyecto(db, proyecto_id)
    if proyecto:
        proyecto.estado = "Eliminado"
        db.commit()
        db.refresh(proyecto)
    return proyecto


def listar_proyectos_eliminados(db: Session):
    """
    Retorna todos los proyectos cuyo estado sea 'Eliminado'.
    Esta función se usa tanto para los reportes como para la vista de proyectos eliminados.
    """
    return db.query(Proyecto).filter(Proyecto.estado == "Eliminado").all()


# Alias para compatibilidad retroactiva con routers antiguos
listar_eliminados = listar_proyectos_eliminados
