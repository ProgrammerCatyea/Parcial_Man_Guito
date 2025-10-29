from pydantic import BaseModel
from typing import Optional

class AsignacionBase(BaseModel):
    proyecto_id: int
    miembro_id: int
    rol: Optional[str] = None

class AsignacionCreate(AsignacionBase):
    pass

class AsignacionResponse(AsignacionBase):
    id: int

    class Config:
        orm_mode = True
