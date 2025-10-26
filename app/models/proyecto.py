from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)
    estado = Column(String(50), nullable=False, default="En progreso")

 
    asignaciones = relationship("Asignacion", back_populates="proyecto", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Proyecto(nombre={self.nombre}, estado={self.estado})>"


class ProyectoEliminado(Base):
    __tablename__ = "proyectos_eliminados"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)
    estado = Column(String(50), nullable=False)
    motivo_eliminacion = Column(String(200), nullable=True)

    def __repr__(self):
        return f"<ProyectoEliminado(nombre={self.nombre}, motivo={self.motivo_eliminacion})>"
