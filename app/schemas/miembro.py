from pydantic import BaseModel
from typing import Optional


class MiembroBase(BaseModel):
    nombre: str
    cargo: str
    especialidad: Optional[str] = None
    estado: Optional[str] = "Activo"


class MiembroCreate(MiembroBase):
    """Schema para crear un nuevo miembro."""
    pass

class MiembroUpdate(BaseModel):
    """Schema para actualizar un miembro existente."""
    nombre: Optional[str] = None
    cargo: Optional[str] = None
    especialidad: Optional[str] = None
    estado: Optional[str] = None


class MiembroResponse(MiembroBase):
    id: int

    class Config:
        orm_mode = True
