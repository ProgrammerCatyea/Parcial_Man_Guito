from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db, Base, engine
from ..schemas.asignacion import AsignacionCreate, AsignacionOut
from ..schemas.miembro import MiembroOut
from ..schemas.proyecto import ProyectoOut
from ..crud import asignacion_crud
from ..core.utils import not_found, conflict

Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/api/asignaciones", tags=["Asignaciones"])

@router.post("/", response_model=AsignacionOut, status_code=201, summary="Asignar miembro a proyecto")
def asignar(payload: AsignacionCreate, db: Session = Depends(get_db)):
    a, err = asignacion_crud.asignar(db, payload.model_dump())
    if err == "miembro_invalido":
        not_found("Miembro")
    if err == "proyecto_invalido":
        not_found("Proyecto")
    if err == "duplicada":
        conflict("El miembro ya está asignado a este proyecto")
    return a

@router.delete("/{asignacion_id}", status_code=204, summary="Desasignar miembro")
def desasignar(asignacion_id: int, db: Session = Depends(get_db)):
    err = asignacion_crud.desasignar(db, asignacion_id)
    if err == "no_encontrado":
        not_found("Asignación")

@router.get("/proyecto/{proyecto_id}/miembros", response_model=List[MiembroOut], summary="Miembros de un proyecto")
def miembros_de_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    miembros, err = asignacion_crud.miembros_de_proyecto(db, proyecto_id)
    if err == "proyecto_invalido":
        not_found("Proyecto")
    return miembros

@router.get("/miembro/{miembro_id}/proyectos", response_model=List[ProyectoOut], summary="Proyectos de un miembro")
def proyectos_de_miembro(miembro_id: int, db: Session = Depends(get_db)):
    proys, err = asignacion_crud.proyectos_de_miembro(db, miembro_id)
    if err == "miembro_invalido":
        not_found("Miembro")
    outs: list[ProyectoOut] = []
    for p in proys:
        outs.append(ProyectoOut(
            id=p.id, nombre=p.nombre, descripcion=p.descripcion, presupuesto=p.presupuesto,
            estado=p.estado, gerente=p.gerente, miembros=[a.miembro for a in p.asignaciones]
        ))
    return outs
