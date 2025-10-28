from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SqlEnum
from app.core.database import Base

class EstadoProyecto(str, Enum):
    EN_PROGRESO = "En progreso"
    COMPLETADO = "Completado"
    CANCELADO = "Cancelado"


class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    estado = Column(SqlEnum(EstadoProyecto), default=EstadoProyecto.EN_PROGRESO)
