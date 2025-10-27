from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from app.core.database import get_db
from app.crud import miembro_crud
from app.schemas.miembro import MiembroCreate, MiembroUpdate
import os

router = APIRouter(
    prefix="/miembros",
    tags=["Miembros"]
)

@router.post("/", response_model=dict)
def crear_miembro(miembro: MiembroCreate, db: Session = Depends(get_db)):
    nuevo = miembro_crud.crear_miembro(db, miembro)
    return {"mensaje": "Miembro creado exitosamente", "data": nuevo}


@router.get("/", response_model=list)
def listar_miembros(db: Session = Depends(get_db)):
    return miembro_crud.obtener_miembros(db)


@router.put("/{miembro_id}", response_model=dict)
def actualizar_miembro(miembro_id: int, miembro: MiembroUpdate, db: Session = Depends(get_db)):
    actualizado = miembro_crud.actualizar_miembro(db, miembro_id, miembro)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    return {"mensaje": "Miembro actualizado correctamente", "data": actualizado}

@router.delete("/{miembro_id}/confirmacion", response_model=dict)
def confirmar_eliminacion(miembro_id: int, db: Session = Depends(get_db)):
    miembro = miembro_crud.obtener_miembro_por_id(db, miembro_id)
    if not miembro:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    return {
        "mensaje": f"¿Seguro que deseas eliminar al miembro '{miembro.nombre}'?",
        "advertencia": "Esta acción moverá al miembro a la lista de eliminados y no podrá recuperarse directamente."
    }


@router.delete("/{miembro_id}", response_model=dict)
def eliminar_miembro(
    miembro_id: int,
    motivo: str = Query("Eliminado manualmente por el usuario"),
    db: Session = Depends(get_db)
):
    eliminado = miembro_crud.eliminar_miembro(db, miembro_id, motivo)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    return {"mensaje": "Miembro eliminado y registrado correctamente", "data": eliminado}


@router.get("/eliminados/", response_model=list)
def listar_eliminados(db: Session = Depends(get_db)):
    return miembro_crud.obtener_miembros_eliminados(db)

@router.get("/reporte/eliminados", response_class=FileResponse)
def descargar_reporte_eliminados(db: Session = Depends(get_db)):
    ruta = miembro_crud.generar_reporte_eliminados(db)
    if not ruta or not os.path.exists(ruta):
        raise HTTPException(status_code=404, detail="No hay miembros eliminados registrados")
    return FileResponse(
        path=ruta,
        filename="reporte_miembros_eliminados.txt",
        media_type="text/plain"
    )
