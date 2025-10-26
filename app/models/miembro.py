from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Miembro(Base):
    __tablename__ = "miembros"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    cargo = Column(String(50), nullable=False)
    especialidad = Column(String(100), nullable=True)
    estado = Column(String(50), default="Activo")

    def __repr__(self):
        return f"<Miembro(nombre={self.nombre}, cargo={self.cargo}, estado={self.estado})>"
