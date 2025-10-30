"""Rutas para la administración de proyectos, con filtrado y control de estado."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from io import StringIO
from fastapi.responses import StreamingResponse

from app.core.database import get_db
from app.schemas.proyecto import ProyectoCreate, ProyectoUpdate, ProyectoResponse
from app.crud.proyecto_crud import (
    listar_proyectos,
    crear_proyecto,
    obtener_proyecto,
    actualizar_proyecto,
    eliminar_proyecto,
    listar_proyectos_eliminados,
    listar_proyectos_activos
)

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])

@router.get("/", response_model=List[ProyectoResponse])
def listar_proyectos_endpoint(
    estado: Optional[str] = Query(None, description="Filtrar por estado (Activo/Inactivo/Eliminado)"),
    presupuesto_min: Optional[float] = Query(None, description="Filtrar por presupuesto mínimo"),
    db: Session = Depends(get_db)
):
    proyectos = listar_proyectos(db, estado=estado, presupuesto_min=presupuesto_min)
    if not proyectos:
        raise HTTPException(status_code=404, detail="No se encontraron proyectos con los filtros aplicados")
    return proyectos

@router.post("/", response_model=ProyectoResponse)
def crear_proyecto_endpoint(proyecto: ProyectoCreate, db: Session = Depends(get_db)):
    nuevo_proyecto = crear_proyecto(db, proyecto)
    return nuevo_proyecto

@router.put("/{proyecto_id}", response_model=ProyectoResponse)
def actualizar_proyecto_endpoint(proyecto_id: int, datos: ProyectoUpdate, db: Session = Depends(get_db)):
    proyecto_existente = obtener_proyecto(db, proyecto_id)
    if not proyecto_existente:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    proyecto_actualizado = actualizar_proyecto(db, proyecto_id, datos)
    return proyecto_actualizado

@router.delete("/{proyecto_id}")
def eliminar_proyecto_endpoint(proyecto_id: int, confirm: bool = False, db: Session = Depends(get_db)):
    proyecto = obtener_proyecto(db, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    if not confirm:
        return {
            "mensaje": f"¿Deseas confirmar la eliminación del proyecto '{proyecto.nombre}'?",
            "confirmar_con": f"/proyectos/{proyecto_id}?confirm=true"
        }

    try:
        eliminado = eliminar_proyecto(db, proyecto_id)
        return {"mensaje": f"Proyecto '{eliminado['nombre']}' marcado como eliminado exitosamente."}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno al eliminar el proyecto: {str(e)}")


@router.get("/eliminados", response_model=List[ProyectoResponse])
def listar_eliminados_endpoint(db: Session = Depends(get_db)):
    eliminados = listar_proyectos_eliminados(db)
    if not eliminados:
        raise HTTPException(status_code=404, detail="No hay proyectos eliminados registrados")
    return eliminados


@router.get("/reporte", response_class=StreamingResponse)
def generar_reporte_proyectos_activos(db: Session = Depends(get_db)):
    proyectos_activos = listar_proyectos_activos(db)
    output = StringIO()

    output.write("REPORTE DE PROYECTOS ACTIVOS\n")
    output.write("===============================\n\n")

    if not proyectos_activos:
        output.write("No hay proyectos activos registrados.\n")
    else:
        for p in proyectos_activos:
            output.write(
                f"ID: {p.id}\n"
                f"Nombre: {p.nombre}\n"
                f"Descripción: {p.descripcion or '—'}\n"
                f"Presupuesto: ${p.presupuesto:,.2f}\n"
                f"Estado: {p.estado}\n"
                f"Fecha de inicio: {p.fecha_inicio or '—'}\n"
                f"Fecha de fin: {p.fecha_fin or '—'}\n"
                f"Gerente ID: {p.id_gerente or '—'}\n"
                f"---------------------------------\n"
            )

    output.seek(0)
    headers = {"Content-Disposition": 'attachment; filename="reporte_proyectos_activos.txt"'}
    return StreamingResponse(iter([output.read()]), media_type="text/plain", headers=headers)

