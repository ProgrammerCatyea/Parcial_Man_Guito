from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Asignacion(Base):
    __tablename__ = "asignaciones"

    id = Column(Integer, primary_key=True, index=True)
    id_proyecto = Column(Integer, ForeignKey("proyectos.id", ondelete="CASCADE"), nullable=False)
    id_miembro = Column(Integer, ForeignKey("miembros.id", ondelete="CASCADE"), nullable=False)
    rol = Column(String, nullable=False)
    fecha_asignacion = Column(Date, nullable=True)

    proyecto = relationship("Proyecto", back_populates="asignaciones")
    miembro = relationship("Miembro", back_populates="asignaciones")
