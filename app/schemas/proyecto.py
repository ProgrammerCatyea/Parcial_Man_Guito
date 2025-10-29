from pydantic import BaseModel
from typing import Optional
from datetime import date


class ProyectoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    estado: Optional[str] = "Activo"
    presupuesto: float
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    id_gerente: Optional[int] = None

class ProyectoCreate(ProyectoBase):
    pass


class ProyectoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[str] = None
    presupuesto: Optional[float] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    id_gerente: Optional[int] = None

class ProyectoResponse(ProyectoBase):
    id: int

    class Config:
        orm_mode = True
