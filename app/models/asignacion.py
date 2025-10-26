from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint
from ..core.database import Base

class Asignacion(Base):
    __tablename__ = "asignaciones"
    __table_args__ = (UniqueConstraint("miembro_id", "proyecto_id", name="uq_miembro_proyecto"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    miembro_id: Mapped[int] = mapped_column(ForeignKey("miembros.id"), nullable=False)
    proyecto_id: Mapped[int] = mapped_column(ForeignKey("proyectos.id"), nullable=False)
    rol_en_proyecto: Mapped[str] = mapped_column(String(60), nullable=False, default="miembro")

    miembro = relationship("Miembro", back_populates="asignaciones")
    proyecto = relationship("Proyecto", back_populates="asignaciones")
