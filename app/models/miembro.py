from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Miembro(Base):
    __tablename__ = "miembros"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    especialidad = Column(String, nullable=True)
    estado = Column(String, default="Activo")

    proyectos_gerente = relationship("Proyecto", back_populates="gerente")
    asignaciones = relationship("Asignacion", back_populates="miembro", cascade="all, delete-orphan")
