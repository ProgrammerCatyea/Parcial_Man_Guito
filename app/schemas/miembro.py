from pydantic import BaseModel, Field
from typing import Optional

class MiembroBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre completo del miembro")
    especialidad: Optional[str] = Field(None, description="Área o rol principal del miembro (ej. Backend, DevOps)")
    estado: Optional[str] = Field("Activo", description="Estado del miembro (Activo o Eliminado)")

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


