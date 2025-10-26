from sqlalchemy import Column, Integer, String, Text, Date, Enum
from app.core.database import Base
import enum

class EstadoProyecto(str, enum.Enum):
    PLANIFICADO = "Planificado"
    EN_PROGRESO = "En Progreso"
    FINALIZADO = "Finalizado"
    CANCELADO = "Cancelado"

class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_inicio = Column(Date, nullable=True)
    fecha_fin = Column(Date, nullable=True)
    estado = Column(Enum(EstadoProyecto), default=EstadoProyecto.PLANIFICADO)
