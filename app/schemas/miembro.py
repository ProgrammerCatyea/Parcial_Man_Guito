from pydantic import BaseModel, Field
from typing import Optional


class MiembroBase(BaseModel):
    nombre: str = Field(..., description="Nombre completo del miembro")
    especialidad: Optional[str] = Field(None, description="Especialidad o rol del miembro (Backend, Frontend, etc.)")
    estado: Optional[str] = Field("Activo", description="Estado actual del miembro (Activo/Inactivo)")


class MiembroCreate(MiembroBase):
    pass

class MiembroUpdate(BaseModel):
    nombre: Optional[str] = None
    especialidad: Optional[str] = None
    estado: Optional[str] = None

class MiembroResponse(MiembroBase):
    id: int

    class Config:
        from_attributes = True

