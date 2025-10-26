from pydantic import BaseModel
from typing import Optional

class AsignacionCreate(BaseModel):
    miembro_id: int
    proyecto_id: int
    rol_en_proyecto: str = "miembro"

class AsignacionOut(BaseModel):
    id: int
    miembro_id: int
    proyecto_id: int
    rol_en_proyecto: str
    class Config:
        from_attributes = True
