from sqlalchemy.orm import Session
from app.models.miembro import Miembro, MiembroEliminado
from app.schemas.miembro import MiembroCreate, MiembroUpdate

def crear_miembro(db: Session, miembro: MiembroCreate):
    nuevo_miembro = Miembro(
        nombre=miembro.nombre,
        rol=miembro.rol,
        correo=miembro.correo
    )
    db.add(nuevo_miembro)
    db.commit()
    db.refresh(nuevo_miembro)
    return nuevo_miembro


def obtener_miembros(db: Session):
    return db.query(Miembro).all()


def obtener_miembro_por_id(db: Session, miembro_id: int):
    return db.query(Miembro).filter(Miembro.id == miembro_id).first()


def actualizar_miembro(db: Session, miembro_id: int, miembro_actualizado: MiembroUpdate):
    miembro = db.query(Miembro).filter(Miembro.id == miembro_id).first()
    if not miembro:
        return None

    for key, value in miembro_actualizado.dict(exclude_unset=True).items():
        setattr(miembro, key, value)

    db.commit()
    db.refresh(miembro)
    return miembro


def eliminar_miembro(db: Session, miembro_id: int, motivo: str = "Sin motivo especificado"):
    miembro = db.query(Miembro).filter(Miembro.id == miembro_id).first()
    if not miembro:
        return None

    eliminado = MiembroEliminado(
        nombre=miembro.nombre,
        rol=miembro.rol,
        correo=miembro.correo,
        motivo_eliminacion=motivo
    )

    db.add(eliminado)
    db.delete(miembro)
    db.commit()
    return eliminado


def obtener_miembros_eliminados(db: Session):
    return db.query(MiembroEliminado).all()


def generar_reporte_eliminados(db: Session, ruta_archivo: str = "reporte_miembros_eliminados.txt"):
    eliminados = db.query(MiembroEliminado).all()
    if not eliminados:
        return None

    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        archivo.write("=== REPORTE DE MIEMBROS ELIMINADOS ===\n\n")
        for m in eliminados:
            archivo.write(f"ID: {m.id}\n")
            archivo.write(f"Nombre: {m.nombre}\n")
            archivo.write(f"Rol: {m.rol}\n")
            archivo.write(f"Correo: {m.correo}\n")
            archivo.write(f"Motivo: {m.motivo_eliminacion}\n")
            archivo.write("-" * 40 + "\n")
    return ruta_archivo
