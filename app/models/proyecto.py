from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.core.database import Base

class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    estado = Column(String, default="Activo")  
    presupuesto = Column(Float, nullable=False)
    fecha_inicio = Column(Date, nullable=True)
    fecha_fin = Column(Date, nullable=True)
    id_gerente = Column(Integer, ForeignKey("miembros.id", ondelete="SET NULL"), nullable=True)

 
    gerente = relationship(
        "Miembro",
        back_populates="proyectos_gerente",
        lazy="joined"
    )

    asignaciones = relationship(
        "Asignacion",
        back_populates="proyecto",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def __repr__(self):
        return f"<Proyecto(id={self.id}, nombre='{self.nombre}', estado='{self.estado}')>"
