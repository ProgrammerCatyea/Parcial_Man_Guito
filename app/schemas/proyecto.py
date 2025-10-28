from pydantic import BaseModel
from typing import Optional
from app.models.proyecto import EstadoProyecto


class ProyectoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    estado: Optional[EstadoProyecto] = EstadoProyecto.EN_PROGRESO

class ProyectoCreate(ProyectoBase):
    pass


class ProyectoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[EstadoProyecto] = None


class ProyectoResponse(ProyectoBase):
    id: int

    class Config:
        from_attributes = True  

class ProyectoOut(BaseModel):
    id: int
    nombre: str
    estado: EstadoProyecto

    class Config:
        from_attributes = True
