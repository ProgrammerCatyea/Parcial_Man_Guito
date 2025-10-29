from pydantic import BaseModel, Field
from typing import Optional

class MiembroBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre completo del miembro")
    especialidad: Optional[str] = Field(None, description="Área o especialidad del miembro")
    estado: Optional[str] = Field("Activo", description="Estado del miembro (Activo/Eliminado)")


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


class MiembroOut(BaseModel):
    id: int
    nombre: str
    especialidad: Optional[str] = None

    class Config:
        from_attributes = True
