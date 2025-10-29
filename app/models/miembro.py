from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Miembro(Base):
    __tablename__ = "miembros"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    rol = Column(String(100), nullable=False)
    correo = Column(String(120), unique=True, nullable=False)
   
    asignaciones = relationship("Asignacion", back_populates="miembro", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Miembro(nombre={self.nombre}, rol={self.rol})>"

class MiembroEliminado(Base):
    __tablename__ = "miembros_eliminados"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    rol = Column(String(100), nullable=False)
    correo = Column(String(120), nullable=False)
    motivo_eliminacion = Column(String(200), nullable=True)

    def __repr__(self):
        return f"<MiembroEliminado(nombre={self.nombre}, motivo={self.motivo_eliminacion})>"
