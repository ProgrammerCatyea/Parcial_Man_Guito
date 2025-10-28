from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.miembro_crud import (
    crear_miembro,
    obtener_miembros,
    actualizar_miembro,
    eliminar_miembro,
    obtener_miembros_eliminados,
    generar_reporte_miembros,
)
from app.schemas.miembro import MiembroCreate, MiembroUpdate, MiembroResponse
from fastapi.responses import FileResponse

router = APIRouter(prefix="/miembros", tags=["Miembros"])

@router.post("/", response_model=MiembroResponse)
def crear_nuevo_miembro(miembro: MiembroCreate, db: Session = Depends(get_db)):
    return crear_miembro(db, miembro)

@router.get("/", response_model=list[MiembroResponse])
def listar_miembros(db: Session = Depends(get_db)):
    return obtener_miembros(db)

@router.put("/{miembro_id}", response_model=MiembroResponse)
def editar_miembro(miembro_id: int, datos: MiembroUpdate, db: Session = Depends(get_db)):
    return actualizar_miembro(db, miembro_id, datos)

@router.delete("/{miembro_id}")
def eliminar_miembro_por_id(miembro_id: int, db: Session = Depends(get_db)):
    return eliminar_miembro(db, miembro_id)

@router.get("/eliminados", response_model=list[MiembroResponse])
def listar_miembros_eliminados(db: Session = Depends(get_db)):
    return obtener_miembros_eliminados(db)

@router.get("/reporte", response_class=FileResponse)
def descargar_reporte_miembros(db: Session = Depends(get_db)):
    ruta_reporte = generar_reporte_miembros(db)
    return FileResponse(ruta_reporte, media_type="text/plain", filename="reporte_miembros.txt")
