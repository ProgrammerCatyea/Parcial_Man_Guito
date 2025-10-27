from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from app.core.database import get_db
from app.crud import proyecto_crud
from app.schemas.proyecto import ProyectoCreate, ProyectoUpdate
import os

router = APIRouter(
    prefix="/proyectos",
    tags=["Proyectos"]
)

@router.post("/", response_model=dict)
def crear_proyecto(proyecto: ProyectoCreate, db: Session = Depends(get_db)):
    nuevo = proyecto_crud.crear_proyecto(db, proyecto)
    return {"mensaje": "Proyecto creado exitosamente", "data": nuevo}

@router.get("/", response_model=list)
def listar_proyectos(db: Session = Depends(get_db)):
    return proyecto_crud.obtener_proyectos(db)


@router.put("/{proyecto_id}", response_model=dict)
def actualizar_proyecto(proyecto_id: int, proyecto: ProyectoUpdate, db: Session = Depends(get_db)):
    actualizado = proyecto_crud.actualizar_proyecto(db, proyecto_id, proyecto)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return {"mensaje": "Proyecto actualizado correctamente", "data": actualizado}


@router.delete("/{proyecto_id}/confirmacion", response_model=dict)
def confirmar_eliminacion(proyecto_id: int, db: Session = Depends(get_db)):
    proyecto = proyecto_crud.obtener_proyecto_por_id(db, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return {
        "mensaje": f"¿Seguro que deseas eliminar el proyecto '{proyecto.nombre}'?",
        "advertencia": "Esta acción moverá el proyecto a la lista de eliminados y no podrá recuperarse directamente."
    }


@router.delete("/{proyecto_id}", response_model=dict)
def eliminar_proyecto(
    proyecto_id: int,
    motivo: str = Query("Eliminado manualmente por el usuario"),
    db: Session = Depends(get_db)
):
    eliminado = proyecto_crud.eliminar_proyecto(db, proyecto_id, motivo)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return {"mensaje": "Proyecto eliminado y registrado correctamente", "data": eliminado}


@router.get("/eliminados/", response_model=list)
def listar_eliminados(db: Session = Depends(get_db)):
    return proyecto_crud.obtener_proyectos_eliminados(db)



@router.get("/reporte/eliminados", response_class=FileResponse)
def descargar_reporte_eliminados(db: Session = Depends(get_db)):
    ruta = proyecto_crud.generar_reporte_eliminados(db)
    if not ruta or not os.path.exists(ruta):
        raise HTTPException(status_code=404, detail="No hay proyectos eliminados registrados")
    return FileResponse(
        path=ruta,
        filename="reporte_proyectos_eliminados.txt",
        media_type="text/plain"
    )
