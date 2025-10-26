from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from app.models.proyecto import EstadoProyecto


class ProyectoBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100, description="Nombre del proyecto")
    descripcion: Optional[str] = Field(None, description="Descripción breve del proyecto")
    fecha_inicio: Optional[date] = Field(None, description="Fecha de inicio del proyecto")
    fecha_fin: Optional[date] = Field(None, description="Fecha estimada de finalización")
    estado: Optional[EstadoProyecto] = Field(default=EstadoProyecto.PLANIFICADO, description="Estado actual del proyecto")

class ProyectoCreate(ProyectoBase):
    """Datos requeridos para crear un nuevo proyecto."""
    pass


class ProyectoUpdate(BaseModel):
    """Datos opcionales para actualizar un proyecto existente."""
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    estado: Optional[EstadoProyecto] = None


class ProyectoResponse(ProyectoBase):
    """Datos devueltos al cliente."""
    id: int

    class Config:
        from_attributes = True


class ProyectoOut(BaseModel):
    """Versión simplificada de proyecto para mostrar dentro de una asignación."""
    id: int
    nombre: str
    estado: Optional[EstadoProyecto] = None

    class Config:
        from_attributes = True
