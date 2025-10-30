from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class ProyectoBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=120, description="Nombre del proyecto")
    descripcion: Optional[str] = Field(None, description="Descripción breve del proyecto")
    estado: Optional[str] = Field("Activo", description="Estado del proyecto (Activo, Inactivo, Eliminado)")
    presupuesto: float = Field(..., ge=0, description="Presupuesto asignado al proyecto")
    fecha_inicio: Optional[date] = Field(None, description="Fecha de inicio del proyecto")
    fecha_fin: Optional[date] = Field(None, description="Fecha de finalización del proyecto")
    id_gerente: Optional[int] = Field(None, description="ID del miembro asignado como gerente")


class ProyectoCreate(ProyectoBase):
    """Esquema para crear un nuevo proyecto."""
    pass


class ProyectoUpdate(BaseModel):
    """Esquema para actualizar parcialmente un proyecto existente."""
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[str] = None
    presupuesto: Optional[float] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    id_gerente: Optional[int] = None


class ProyectoResponse(ProyectoBase):
    """Respuesta del servidor con los datos del proyecto."""
    id: int

    class Config:
        from_attributes = True 
