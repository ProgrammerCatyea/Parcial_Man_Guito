from pydantic import BaseModel
from typing import Optional
from datetime import date

class AsignacionBase(BaseModel):
    id_proyecto: int
    id_miembro: int
    rol: str
    fecha_asignacion: Optional[date] = None

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
        orm_mode = True
