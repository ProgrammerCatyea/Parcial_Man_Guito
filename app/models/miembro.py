from sqlalchemy import Column, Integer, String, Float, Enum
from app.core.database import Base
import enum

class EstadoMiembro(enum.Enum):
    ACTIVO = "Activo"
    ELIMINADO = "Eliminado"

class Miembro(Base):
    __tablename__ = "miembros"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    especialidad = Column(String, nullable=False)
    salario = Column(Float, nullable=False)
    estado = Column(Enum(EstadoMiembro), default=EstadoMiembro.ACTIVO)
