from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class AsignacionBase(BaseModel):
    id_proyecto: int = Field(..., description="ID del proyecto asociado")
    id_miembro: int = Field(..., description="ID del miembro asignado")
    rol: str = Field(..., min_length=2, max_length=100, description="Rol dentro del proyecto")
    fecha_asignacion: Optional[date] = Field(None, description="Fecha de asignación (opcional)")


class AsignacionCreate(AsignacionBase):

    pass

class AsignacionUpdate(BaseModel):

    id_proyecto: Optional[int] = None
    id_miembro: Optional[int] = None
    rol: Optional[str] = None
    fecha_asignacion: Optional[date] = None


class AsignacionResponse(AsignacionBase):
   
    id: int
    class Config:
        from_attributes = True 
