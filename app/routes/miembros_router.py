from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.miembro import MiembroCreate, MiembroUpdate
from app.crud.miembro_crud import (
    obtener_miembros,
    crear_miembro,
    actualizar_miembro,
    eliminar_miembro
)

router = APIRouter(prefix="/miembros", tags=["Miembros"])

@router.get("/", status_code=status.HTTP_200_OK)
def listar_miembros(db: Session = Depends(get_db)):
    return obtener_miembros(db)

@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_miembro_endpoint(miembro_data: MiembroCreate, db: Session = Depends(get_db)):
    try:
        return crear_miembro(db, miembro_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.put("/{miembro_id}", status_code=status.HTTP_200_OK)
def actualizar_miembro_endpoint(miembro_id: int, miembro_data: MiembroUpdate, db: Session = Depends(get_db)):
    try:
        return actualizar_miembro(db, miembro_id, miembro_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.delete("/{miembro_id}", status_code=status.HTTP_200_OK)
def eliminar_miembro_endpoint(miembro_id: int, db: Session = Depends(get_db)):
    try:
        return eliminar_miembro(db, miembro_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
