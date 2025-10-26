from pydantic import BaseModel, Field
from typing import Optional

class MiembroBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=120)
    rol_general: str = Field(min_length=2, max_length=80)
    estado: str = Field(pattern="^(activo|inactivo)$")

class MiembroCreate(MiembroBase):
    pass

class MiembroUpdate(BaseModel):
    nombre: Optional[str] = None
    rol_general: Optional[str] = None
    estado: Optional[str] = None

class MiembroOut(MiembroBase):
    id: int
    class Config:
        from_attributes = True
