from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class MiembroBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre completo del miembro")
    cargo: Optional[str] = Field(None, description="Cargo o rol dentro de la organización")
    correo: EmailStr = Field(..., description="Correo electrónico del miembro")


class MiembroCreate(MiembroBase):
    """Datos requeridos para crear un nuevo miembro."""
    pass


class MiembroUpdate(BaseModel):
    """Datos opcionales para actualizar un miembro existente."""
    nombre: Optional[str] = None
    cargo: Optional[str] = None
    correo: Optional[EmailStr] = None


class MiembroResponse(MiembroBase):
    """Datos devueltos al cliente al consultar miembros."""
    id: int

    class Config:
        from_attributes = True




class MiembroOut(BaseModel):
    """Versión resumida para mostrar dentro de asignaciones."""
    id: int
    nombre: str
    cargo: Optional[str] = None

    class Config:
        from_attributes = True
