from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class EstadoProyecto(enum.Enum):
    EN_PROGRESO = "En progreso"
    FINALIZADO = "Finalizado"
    ELIMINADO = "Eliminado"

class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    descripcion = Column(String)
    presupuesto = Column(Float, nullable=False)
    estado = Column(Enum(EstadoProyecto), default=EstadoProyecto.EN_PROGRESO)

    gerente_id = Column(Integer, ForeignKey("miembros.id"))
    gerente = relationship("Miembro", backref="proyectos_gerente")

